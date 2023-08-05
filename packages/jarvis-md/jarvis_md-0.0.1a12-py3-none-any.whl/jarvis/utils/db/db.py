import os, glob, yaml, numpy as np, pandas as pd, tarfile
from .query import find_matching_files
from . import funcs
from ..general import printd, printp, tools as jtools
from ..display import interleave

# ===================================================================
# OVERVIEW
# ===================================================================
# 
# DB is an object that facilitates interaction and manipulation
# of data serialized in a way that conforms to the standard Jarvis 
# file directory hiearchy. Two primary forms of data are indexed:
#
#   (1) fnames ==> index of file locations
#   (2) header ==> index of metadata for each file 
# 
# The underlying indexed data is stored as CSV files. 
# 
# ===================================================================
# 
# [ FILE-SYS ] \
#               <----> [ CSV-FILE ] <----> [ -CLIENT- ] 
# [ MONGO_DB ] /
# 
# ===================================================================

class DB():

    def __init__(self, *args, **kwargs):
        """
        Method to initialize DB() object

        :params

          (str)  yml         : full path to DB *.yml file (most common method)
          (str)  csv         : full path to DB *.csv file (no *.yml information)
          (str)  project_id  : Jarvis project ID (used when defining new DB object); otherwise extracted from *.yml
          (str)  version_id  : Jarvis version ID (used when defining new DB object); otherwise extracted from *.yml
          (str)  prefix      : common prefix to *.yml / *.csv files (alternative to explicit *.yml file)
          (str)  subdir      : common subdir to *.yml / *.csv files (alternative to explicit *.yml file)
          (df)   fnames      : Pandas DataFrame with fnames to init new DB object
          (df)   header      : Pandas DataFrame with header to init new DB object
          (dict) sform       : manual sform definitions to init new DB object 
          (dict) fdefs       : manual fdefs definitions to init new DB object 
          (bool) rewrite     : by default, new data is appended to existing files; if True, rewrite existing files

        """
        # --- Initialize db 
        self.init_db(*args, **kwargs)

        # --- Load YML and CSV files
        rewrite = kwargs.pop('rewrite', False)
        self.load_yml(rewrite=rewrite)
        self.load_csv(rewrite=rewrite, **kwargs)

        # --- Refresh
        self.init_fdefs()
        self.refresh()

    def init_db(self, *args, **kwargs):
        """
        Method to initialize DB() configurations

        """
        # --- Attributes to serialize in self.to_yml(...) 
        self.ATTRS = ['_id', 'files', 'query', 'sform', 'fdefs']

        DEFAULTS = {
            'query': {},
            'sform': {},
            'fdefs': []}

        # --- Initialize configs 
        configs = jtools.parse_args(*args, **kwargs)

        # --- Initialize default values
        configs = {**DEFAULTS, **kwargs, **configs} 

        # --- Parse remaining args 
        for arg in args:
            if type(arg) is dict:
                configs['query'] = arg
                if 'root' in configs['query']:
                    configs['paths']['data'] = configs['query'].pop('root')

            if type(arg) is list:
                configs['fdefs'] = arg

        # --- Load custom functions
        self.load_func = kwargs.pop('load', None) 
        self.save_func = kwargs.pop('save', None) 

        # --- Set attributes 
        for attr in self.ATTRS:
            setattr(self, attr, configs[attr])

        self.paths = configs['paths']

        return configs 

    def load_paths(self, alt_path=None):
        """
        Method to load paths from project_id if not already existing 

        """
        if self.paths['code'] != '' and self.paths['data'] != '':
            return

        # --- Load paths
        self.paths.update(jtools.get_paths(
            project_id=self._id['project'], 
            version_id=self._id['version'],
            alt_path=alt_path))

    def save_paths(self, paths=None, project_id=None, version_id=None, update_fnames=False):
        """
        Method to save paths (either in self.paths or newly provided paths kwarg)

        """
        # --- Prepare paths
        paths = paths or self.paths
        project_id = project_id or self._id['project']
        version_id = version_id or self._id['version']

        if project_id is None:
            printd('ERROR either project_id must already exist in DB or be manually provided')
            return

        # --- Set paths
        paths = jtools.set_paths(paths, project_id, version_id)
        self.set_paths(paths)

        # --- Update _id
        self._id = {
            'project': project_id,
            'version': version_id}

        # --- Update fnames
        if update_fnames:
            for col in self.fnames:
                self.update_fnames(col, self.sform.get(col, '{curr}'))

    def set_paths(self, paths):
        """
        Method to set new paths to self.paths

        :params

          (dict) paths : {'data': ..., 'code': ...}, OR
          (str)  paths : same path is inferred for both data and code 

        """
        if type(paths) is str:
            paths = {'data': paths, 'code': paths}
        else:
            assert type(paths) is dict
            paths = {**self.paths, **paths}

        # --- Retrieve current files
        files = self.get_files()

        self.paths['data'] = os.path.abspath(paths['data'])
        self.paths['code'] = os.path.abspath(paths['code'])

        # --- Update files
        self.set_files(files)

    def get_paths(self, paths):
        """
        Method to get paths

        """
        return self.paths.copy()

    def set_files(self, files=None, subdir='.'):
        """
        Method to set new files to self.files

        :params

          (dict) files : {'csv': ..., 'yml': ...}, OR
          (str)  files : inferred string pattern e.g. 'db-all' 

        """
        if type(files) is str:
            files = {
                'csv': '{}/csvs/{}.csv.gz'.format(subdir, files),
                'yml': '{}/ymls/{}.yml'.format(subdir, files)}

        else:
            files = {**self.files, **(files or {})} 

        # --- Expand and replace paths
        trim = lambda x : os.path.abspath(x).replace(self.paths['code'], '', 1)

        self.files['yml'] = trim(files['yml']) if files['yml'] is not None else None
        self.files['csv'] = trim(files['csv']) if files['csv'] is not None else None

    def get_files(self):
        """
        Method to get full file paths

        """
        return {k: '{}{}'.format(self.paths['code'], v) for k, v in self.files.items()}

    # ===================================================================
    # YML | LOAD
    # ===================================================================

    def load_yml(self, fname=None, rewrite=False):
        """
        Method to load YML file

        """
        fname = fname or self.get_files()['yml'] or ''

        if os.path.exists(fname) and not rewrite:
            with open(fname, 'r') as y:
                configs = yaml.load(y, Loader=yaml.FullLoader)

            for attr, config in configs.items():
                setattr(self, attr, config)

        # --- Load paths / files
        self.load_paths(alt_path=fname)
        self.set_files()

    # ===================================================================
    # CSV | LOAD and PREPARE
    # ===================================================================

    def load_csv(self, fname=None, lazy=True, rewrite=False, **kwargs):
        """
        Method to load CSV file

        """
        self.fnames_expanded = {} 

        # --- Initialize from manually passed kwargs if possible
        if 'fnames' in kwargs:
            self.fnames = kwargs.pop('fnames', None)
            self.header = kwargs.pop('header', pd.DataFrame(index=self.fnames.index))

            self.fnames.index.name = 'sid'
            self.header.index.name = 'sid'

            return

        fname = fname or self.get_files()['csv'] or ''

        if os.path.exists(fname) and not rewrite:
            df = pd.read_csv(fname, index_col='sid', keep_default_na=False)
        else: 
            df = pd.DataFrame()
            df.index.name = 'sid'

        # --- Split df into fnames and header 
        self.fnames, self.header = self.df_split(df)

        # --- Load full fnames 
        if not lazy:
            self.fnames = self.fnames_expand()
            self.sform = {}

    def df_split(self, df):
        """
        Method to split DataFrame into `fnames` + `header`

        """
        fnames = df[[k for k in df if k[:6] == 'fname-']]
        header = df[[k for k in df if k not in fnames]]

        # --- Rename `fnames-`
        fnames = fnames.rename(columns={k: k[6:] for k in fnames.columns})

        return fnames, header 

    def df_merge(self, rename=False):
        """
        Method to merge DataFrame

        """
        # --- Rename `fnames-`
        if rename:
            c = {k: 'fname-%s' % k for k in self.fnames.columns}
            fnames = self.fnames.rename(columns=c)
        else:
            fnames = self.fnames

        # --- Determine need for sort
        sort = ~(fnames.index == self.header.index).all()

        return pd.concat((fnames, self.header), axis=1, sort=sort)

    # ===================================================================
    # REFRESH | SYNC WITH FILE SYSTEM 
    # ===================================================================

    def refresh(self, cols=None, fdefs=None, load=None, update_query=False, **kwargs):
        """
        Method to refresh DB() object 

        """
        # --- Update query 
        if self.fnames.shape[0] == 0 or update_query:
            self.update_query()

        if fdefs is not None:
            # --- Create columns via fdefs
            self.create_column(fdefs=fdefs, load=load, **kwargs)

        else:
            # --- Create columns via defs
            cols = cols or []
            if type(cols) is str:
                cols = [cols]

            for col in cols:
                self.create_column(col=col, load=load, **kwargs)

    def update_query(self, matches=None):
        """
        Method to refresh rows by updating with results of query

        """
        if len(self.query) == 0 and matches is None:
            return

        # --- Query for matches
        if matches is None:
            query = self.query.copy()
            query['root'] = self.paths['data']
            matches, _ = find_matching_files(query, verbose=False)

        self.fnames = pd.DataFrame.from_dict(matches, orient='index')

        # --- Propogate indices if meta is empty 
        if self.header.shape[0] == 0:
            self.header = pd.DataFrame(index=self.fnames.index)

        self.fnames.index.name = 'sid'
        self.header.index.name = 'sid'

    def create_column(self, col=None, fdefs=None, load=None, mask=None, indices=None, split=None, splits=None, flush=False, replace=True, skip_existing=True, **kwargs):
        """
        Method to create column

        """
        # --- Initialize fdefs
        fdefs = self.find_fdefs(col) if fdefs is None else funcs.init(fdefs, root=self.paths['code'])

        if len(fdefs) == 0:
            return

        use_cache = kwargs.get('clear_arrays', True)
        for sid, fnames, header in self.cursor(mask=mask, indices=indices, flush=flush, split=split, splits=splits, use_cache=use_cache):

            if col is not None:
                update = not os.path.exists(fnames[col]) if col in fnames else header[col] == ''
            else:
                update = True

            if update or not skip_existing:
                self.apply_row(sid, fdefs, load=load, fnames=fnames, header=header, replace=replace, **kwargs)

    # ===================================================================
    # FDEFS FUNCTIONS 
    # ===================================================================

    def init_fdefs(self):
        """
        Method to initialize self.fdefs

        """
        # --- Create col_to_fdef dict
        self.col_to_fdef = {}
        for n, fdef in enumerate(self.fdefs):

            # --- Map column returns
            if 'return' in fdef:
                for v in fdef['return'].values():
                    self.col_to_fdef[v] = n 

            # --- Expand any filenames
            if 'python' in fdef:
                if fdef['python'] is not None:
                    assert 'file' in fdef['python']
                    if '{root}' not in fdef['python']['file']:
                        fdef['python']['file'] = '{root}/data' + fdef['python']['file']

    def find_fdefs(self, cols):
        """
        Method to find and initialize all fdefs corresponding to provided columns

        """
        if type(cols) is str:
            cols = [cols]

        fdefs = []
        for col in cols:
            if col in self.col_to_fdef:

                fdef = self.col_to_fdef[col]

                # --- Initialize if needed
                if type(fdef) is int:
                    rets = self.fdefs[fdef]['return'].values()
                    fdef = funcs.init([self.fdefs[fdef]], root=self.paths['code'])
                    self.col_to_fdef.update({k: fdef for k in rets})

                fdefs += fdef

        return fdefs

    # ===================================================================
    # FNAMES FUNCTIONS 
    # ===================================================================

    def exists(self, cols=None, verbose=True, ret=False):
        """
        Method to check if fnames exists

        """
        exists = {}
        fnames = self.fnames_expand(cols=cols)
        ljust = max([len(c) for c in fnames.columns])

        for col in fnames.columns:
            exists[col] = fnames[col].apply(lambda x : os.path.exists(x)).to_numpy()

            if verbose:
                printd('COLUMN: {} | {:06d} / {:06d} exists'.format(col.ljust(ljust), exists[col].sum(), fnames[col].shape[0]))

        if ret:
            return exists

    def fnames_like(self, suffix, like=None):
        """
        Method to create new fnames in pattern based on column defined by like

        """
        like = like or self.fnames.columns[0]

        return self.fnames[like].apply(lambda x : '{}/{}'.format(os.path.dirname(x), suffix))

    def fnames_expand(self, cols=None, use_cache=True):
        """
        Method to expand fnames based on defined str formats (sform)

        """
        root = self.paths['data']

        if cols is None:
            cols = self.fnames.columns

        if type(cols) is str:
            cols = [cols]

        fnames = pd.DataFrame(index=self.fnames.index)
        fnames.index.name = 'sid'

        for col in cols:
            if (col in self.fnames_expanded) and use_cache:
                fnames[col] = self.fnames_expanded[col]
            
            elif col in self.sform:
                fnames[col] = [self.sform[col].format(root=root, curr=f, sid=s)
                    for s, f in zip(self.fnames.index, self.fnames[col])]
            else:
                fnames[col] = self.fnames[col]

        # --- Retain cache of expanded fnames
        if self.fnames_expanded is {}:
            self.fnames_expanded = fnames
        else:
            for col in fnames:
                self.fnames_expanded[col] = fnames[col]

        return fnames 

    def fnames_expand_single(self, sid=None, index=None, fnames=None):
        """
        Method to expand a single fnames dict based on str formats (sform)

        """
        if fnames is None:

            if index is not None:
                fnames = self.fnames.iloc[index].to_dict()
                sid = self.fnames.index[index]

            else: 
                assert sid is not None
                assert self.fnames.index.is_unique
                fnames = self.fnames.loc[sid].to_dict()

        fnames = fnames or {}

        return {k: self.sform[k].format(root=self.paths['data'], curr=v, sid=sid) 
            if k in self.sform else v for k, v in fnames.items()}

    def restack(self, columns_on, marker=None, suffix=''):
        """
        Method to stack specified columns on existing fname

        All other fnames/header data will be copied from existing row

        :params

          (str) marker : if provided, create new header indicating stack status
          (str) suffix : if provided, suffix to add to index e.g. {sid}-{suffx}{:03d}

        """
        fnames = []
        header = []

        # --- Create new header
        if marker is not None:
            self.header[marker] = False

        # --- Create baseline fnames
        cols_ = [c for cols in columns_on.values() for c in cols]
        fname = [c for c in self.fnames.columns if c not in cols_]
        heads = [c for c in self.header.columns if c not in cols_]
        fnames.append(self.fnames[fname])
        header.append(self.header[heads])

        n = len(next(iter(columns_on.values())))
        for i in range(n):

            f = fnames[0].copy()
            h = header[0].copy()

            for on, cols in columns_on.items():
                if cols[i] in self.fnames:
                    f[on] = self.fnames[cols[i]]
                else:
                    h[on] = self.header[cols[i]]

            index = ['{}-{}{:03d}'.format(sid, suffix, i) for sid in f.index]
            f.index = index
            h.index = index
            f.index.name = 'sid'
            h.index.name = 'sid'

            if marker is not None:
                h[marker] = True
            
            fnames.append(f)
            header.append(h)

        # --- Update index of 0th index
        fnames[0].index = ['{}-{}org'.format(sid, suffix) for sid in fnames[0].index]
        header[0].index = fnames[0].index 

        # -- Combine
        self.fnames = pd.concat(fnames, axis=0)
        self.header = pd.concat(header, axis=0)

        self.fnames_expanded = {}

    def init_sform(self, subdirs=None, json=[], cols=None, proc='/proc/', ignore_cols=[]):
        """
        Method to initialize default sform based of current fnames columns

        Default fnames column format:
        
          [base]-[dirs](-[suffix])

          base ==> used for file basename e.g. dat-xxx = dat.hdf5
          dirs ==> used for subdirectory (inferred by subdirs mapping)

        Default sform format:

          '{root}/proc/{subdir}/{sid}/{base}.{ext}'

        Default extension is *.hdf5 unless base is in JSON list

        """
        cols = cols or self.fnames.columns
        cols = [c for c in cols if (c not in ignore_cols) and (c not in self.sform)]
        json += ['pts', 'box', 'vec']

        # --- Default subdirs mappings
        subdirs = subdirs or {}
        subdirs['dcm'] = 'dcm'
        subdirs['raw'] = 'raw'

        sform = {}

        for col in cols:
            parts = len(col.split('-'))
            if parts > 1:

                # --- Infer subdirectory
                subdir = col.split('-')[1]
                if subdir in subdirs:
                    subdir = subdirs[subdir]

                # --- Infer basename
                base = col.split('-')[0]
                subsid = '-'.join(col.split('-')[2:]) + '/' if parts > 2 else ''

                if base == 'dcm':

                    sform[col] = '{root}%sdcm/{sid}/' % proc

                else:

                    # --- Infer extension
                    ext = 'json' if col.split('-')[0] in json else 'hdf5'

                    # --- Create sform
                    sform[col] = '{{root}}{proc}{subdir}/{{sid}}/{subsid}{base}.{ext}'.format(
                        root='root',
                        proc=proc,
                        subdir=subdir,
                        sid='sid',
                        subsid=subsid,
                        base=base,
                        ext=ext) 

        self.sform.update(sform)

    def update_sform(self, sform='{root}{curr}'):
        """
        Method to update sform for specified columns and corresponding fnames

        :params

          (dict) sform = {
                    [col-00]: [sform-pattern],
                    [col-01]: [sform-pattern],
                    [col-02]: [sform-pattern], ... }

        NOTE: if str is provided, sform pattern is propogated to all columns

        """
        if type(sform) is str:
            sform = {k: sform for k in self.fnames}

        if type(sform) is not dict:
            printd('ERROR, sform is not formatted correctly')
            return

        for col, s in sform.items():
            self.update_fnames(col, s)

        self.sform.update(sform)
        self.fnames_expanded = {} 

    def update_fnames(self, col, sform):
        """
        Method to update fnames column based on provided sform:

          (1) Fully expand current fnames
          (2) Recompress fnames based on new sform

        NOTE: this method is intended as an internal function; it does not update sform
        after manipulation of fnames. The recommended approach for most sform updates
        is the self.update_sform(...) method.

        """
        assert col in self.fnames

        # --- Recompress fnames 
        root = self.paths['data']
        loc_r = sform.find('{root}')
        loc_c = sform.find('{curr}')
        loc_s = sform.find('{sid}')

        # --- CONDITION: all fnames inferred from sform alone (no '{curr}') 
        if (loc_c == -1):
            self.fnames[col] = ''
            return

        # --- CONDITION: only '{curr}' without existing self.sform entry
        if sform == '{curr}' and col not in self.sform:
            return

        # --- Expand fnames (all other conditions require at least this)
        self.fnames[col] = self.fnames_expand(cols=col)

        # --- CONDITION: only '{curr}' with existing self.sform entry
        if sform == '{curr}':
            return

        # --- CONDITION: no '{sid}' and '{curr}' at the end e.g. '{root}{curr}'
        if (loc_s == -1) and (sform[-6:] == '{curr}'):
            prefix = sform[:-6].format(root=root)
            if prefix in self.fnames[col].iloc[0]:
                n = len(prefix)
                self.fnames[col] = self.fnames[col].apply(lambda x : x[n:])

            return

        # --- ELSE: Create generic function for all alternate cases
        prefix, suffix = sform.split('{curr}')

        def recompress(f, sid):
            """
            Method to remove formatted prefix / suffix from string f

            """
            f = f.replace(prefix.format(root=root, sid=sid), '')
            f = f.replace(suffix.format(root=root, sid=sid), '')

            return f
            
        self.fnames[col] = [recompress(f, s) for f, s in zip(self.fnames[col], self.fnames.index)]

    # ===================================================================
    # DATA AUGMENTATION 
    # ===================================================================

    def create_fnames_augmented(self, column, n, basename=None):
        """
        Method to create augmented fnames in the following dir structure:

        /[root]/
          |--- dat.hdf5
          ...
          |--- augs/
               |--- aug-000/
                    |--- dat.hdf5
                    ...
               |--- aug-001/
               |--- aug-002/
               ...

        :params

          (str) column : name of column to augment
          (int) n      : number of augmentations

        """
        assert type(column) is str
        assert type(n) is int
        assert column in self.fnames

        roots = [os.path.dirname(f) for f in self.fnames[column]]
        bases = [os.path.basename(f) for f in self.fnames[column]] if basename is None else [basename] * len(roots)

        keys = ['{}-aug-{:03d}'.format(column, i) for i in range(n)]

        for i, key in enumerate(keys):

            self.fnames[key] = \
                ['{}/augs/aug-{:03d}/{}'.format(r, i, b) for r, b in zip(roots, bases)]

        return keys

    def realign(self, cols, align_with, jars, mask=None, flush=True):
        """
        Method to realign volumes in provided columns with reference volume

        """
        for fname in cols + [align_with]:
            assert fname in self.fnames

        assert hasattr(jars, 'create')

        for sid, fnames, header in self.cursor(mask=mask, flush=flush):

            # --- Load reference volume
            ref = jars.create(fnames[align_with])

            # --- Align and save
            for col in cols:

                arr = jars.create(fnames[col])
                arr = arr.align_with(ref)

                dst = '{}/{}.hdf5'.format(
                    os.path.dirname(fnames[align_with]),
                    os.path.splitext(os.path.basename(fnames[col]))[0])

                arr.to_hdf5(dst)
                self.fnames.at[sid, col] = dst

    # ===================================================================
    # ITERATE AND UPDATES 
    # ===================================================================

    def row(self, index=None, sid=None):
        """
        Method to return single row at self.fnames and self.header

        """
        fnames = self.fnames_expand_single(sid=sid, index=index)
        header = self.header.loc[sid].to_dict() if sid is not None else self.header.iloc[index].to_dict()

        return {**fnames, **header} 

    def cursor(self, mask=None, indices=None, split=None, splits=None, drop_duplicates=False, subset=None, status='Iterating | {:06d}', verbose=True, flush=False, use_cache=True, **kwargs):
        """
        Method to create Python generator to iterate through dataset
        
        """
        count = 0

        df = self.df_merge(rename=False) 
        fcols = self.fnames.columns
        hcols = self.header.columns
        fsize = fcols.size

        # --- Expand fnames
        df[fcols] = self.fnames_expand(cols=fcols, use_cache=use_cache)
        
        # --- Apply mask
        if mask is not None:
            df = df[mask]

        # --- Apply indices
        if indices is not None:
            df = df.iloc[indices]

        # --- Create splits
        if splits is not None:
            r, status = self.create_splits(split, splits, df.shape[0], status)
            df = df.iloc[r]

        # --- Drop duplicates
        if drop_duplicates:
            df = df.drop_duplicates(subset=subset or fcols)

        for tups in df.itertuples():

            if verbose:
                count += 1
                printp(status.format(count), count / df.shape[0], flush=flush)

            fnames = {k: t for k, t in zip(fcols, tups[1:1+fsize])}
            header = {k: t for k, t in zip(hcols, tups[1+fsize:])}

            yield tups[0], fnames, header

    def create_splits(self, split, splits, rows, status):
        """
        Method to identify current split range

        """
        # --- Read from os.environ if None
        if split is None:
            split = int(os.environ.get('JARVIS_SPLIT', 0))

        # --- Create splits
        sp = np.linspace(0, rows, splits + 1)
        sp = np.round(sp).astype('int')

        # --- Update status message
        ss = status.split('|')
        ss[0] = ss[0] + '(split == {}/{}) '.format(split + 1, splits)
        status = '|'.join(ss)

        return range(sp[split], sp[split + 1]), status

    def apply(self, fdefs, load=None, mask=None, indices=None, flush=False, replace=False, **kwargs):
        """
        Method to apply a series of lambda functions
    
        :params

          (str)  fdefs = 'mr_train', 'ct_train', ... OR

          (list) fdefs = [{

            'lambda': 'coord', 'stats', ... OR lambda function,
            'python': {'file': ..., 'name': ...}
            'kwargs': {...},
            'return': {...}

            }]

        See dl_utils.db.funcs.init(...) for more information about fdefs list

        """
        fdefs = funcs.init(fdefs, root=self.paths['code'], **kwargs)

        dfs = []
        for sid, fnames, header in self.cursor(mask=mask, indices=indices, flush=flush):
            dfs.append(self.apply_row(sid, fdefs, load=load, fnames=fnames, header=header, replace=replace))

        return pd.concat(dfs, axis=0)

    def apply_row(self, sid, fdefs, load=None, save=None, fnames=None, header=None, replace=False, clear_arrays=True, rcount=0, **kwargs):
        """
        Method to apply a series of lambda functions to single row

        """
        # --- Set load func
        load = load or self.load_func
        save = save or self.save_func

        if fnames is None:
            sid = sid if sid in self.fnames.index else int(sid)
            fnames = self.fnames_expand_single(sid=sid)

        if header is None:
            sid = sid if sid in self.header.index else int(sid)
            header = self.header.loc[sid] 

        df = pd.DataFrame()
        for fdef in fdefs:

            lambda_ = fdef['lambda']
            kwargs_ = fdef['kwargs']
            return_ = fdef['return']

            in_dict = lambda x, d : x in d if type(x) is str else False

            # --- Load all fnames if load function is provided
            if load is not None:
                to_load = {v: fnames[v] for v in kwargs_.values() if in_dict(v, fnames) and type(fnames[v]) is str}
                for key, fname in to_load.items():
                    if os.path.exists(fname):
                        fnames[key] = load(fname)
                        if type(fnames[key]) is tuple:
                            fnames[key] = fnames[key][0]

                    else:
                        # --- Recursively create new fnames 
                        fdefs = self.find_fdefs(cols=key)
                        if len(fdefs) > 0: 
                            rcount += 1
                            df_ = self.apply_row(sid, fdefs, load=load, fnames=fnames, header=header, replace=replace, clear_arrays=False, rcount=count)
                            if df_.shape[0] > 0:
                                fnames.update({k: v for k, v in df_.iloc[0].items() if k in fnames and v is not None})
                        else:
                            if rcount > 0:
                                return pd.DataFrame(index=[sid]) 

            # --- Ensure all kwargs values are hashable
            kwargs_ = {k: tuple(v) if type(v) is list else v for k, v in kwargs_.items()}

            fs = {k: fnames[v] for k, v in kwargs_.items() if in_dict(v, fnames)}
            hs = {k: header[v] for k, v in kwargs_.items() if in_dict(v, header)}

            ds = lambda_(**dict({**kwargs_, **fs, **hs}))

            # --- Update df
            if len(return_) == 0:
                return_ = {k: k for k in ds.keys()}

            # --- Create DataFrame 
            if df.size == 0:
                ds = {k: v if (hasattr(v, '__iter__') or return_.get(k, None) in fnames) else [v] for k, v in ds.items()}
                ln = lambda x : len(x) if hasattr(x, '__len__') else 1
                mx = max([ln(v) for v in ds.values()]) if len(ds) > 0 else 1
                df = pd.DataFrame(index=[sid] * mx)
                df.index.name = 'sid'

            keys = sorted(return_.keys())
            for key in keys:

                # --- For fnames, put entire single object into Pandas cell
                if return_[key] in fnames:
                    df[return_[key]] = ''
                    df.at[sid, return_[key]] = ds.get(key, None)

                # --- For header, put single value or iterable in Pandas cell(s)
                else:
                    df[return_[key]] = ds.get(key, None)

        # --- In-place replace if df.shape[0] == 1
        if replace and df.shape[0] == 1:
            for key, col in df.items():

                # --- Save fnames
                if key in fnames:
                    if type(fnames[key]) is str:
                        if len(fnames[key]) > 0:

                            # --- Check default save
                            if save is not None:
                                save(fnames[key], col.values[0])

                            # --- Check default methods
                            else:
                                for method in ['to_hdf5', 'to_json']:
                                    if hasattr(col.values[0], method):
                                        getattr(col.values[0], method)(fnames[key])
                                        break
                            
                    if clear_arrays:
                        df.at[sid, key] = fnames[key]
                    else:
                        if df.at[sid, key] is not None:
                            self.fnames.at[sid, key] = df.at[sid, key]
                            self.sform.pop(key, None)

                # --- Save header
                if key in header:
                    self.header.at[sid, key] = col.values[0]

        return df

    def query(self):
        """
        Method to query db for data

        """
        pass

    def montage(self, dat, lbl=None, point=(0.5, 0.5, 0.5), shape=(1, 0, 0), N=None, load=None, func=None, **kwargs):
        """
        Method to load montage of database

        """
        # --- Set load func
        load = load or self.load_func
        if load is None:
            return

        # --- Unravel tuples
        unravel = lambda x : x[0] if type(x) is tuple else x

        # --- Aggregate
        dats, lbls = [], []

        # --- Initialize default kwargs
        if 'mask' not in kwargs and 'indices' not in kwargs and N is not None:
            kwargs['indices'] = np.arange(N ** 2)

        for sid, fnames, header in self.cursor(**kwargs):

            # --- Load dat
            infos = {'point': point, 'shape': shape} if func is None else None
            d = unravel(load(fnames[dat], infos=infos, **kwargs))
            if d is not None:

                dats.append(d)

                # --- Load lbl
                if lbl is not None:
                    infos = {'point': point, 'shape': shape} if func is None else None
                    l = unravel(load(fnames[lbl], infos=infos, **kwargs)) 
                    lbls.append(l)

                    # --- Apply label conversion and slice extraction function
                    if func is not None:
                        dats[-1], lbls[-1] = func(dat=d, lbl=l, sid=sid, **kwargs)

                # --- Extract np.ndarray if needed
                if type(dats[-1]) is not np.ndarray and hasattr(dats[-1], 'data'):
                    dats[-1] = dats[-1].data
                    if len(lbls) > 0:
                        lbls[-1] = lbls[-1].data 

        # --- Interleave dats
        dats = interleave(np.stack(dats), N=N)

        # --- Interleave lbls
        if lbl is not None:
            lbls = interleave(np.stack(lbls), N=N)

        return dats, lbls

    # ===================================================================
    # CREATE SUMMARY DB 
    # ===================================================================

    def create_summary(self, fdefs, fnames=[], header=[], folds=5, prefix='db-sum', subdir='data', **kwargs):
        """
        Method to generate summary training stats via self.apply(...) operation

        :params

          (dict) kwargs : kwargs initialized via funcs.init(...)
          (list) fnames : list of fnames to join
          (list) header : list of header columns to join

          (int)  folds  : number of cross-validation folds
          (str)  path   : directory path to save summary (ymls/ and csvs/)

        """
        df = self.apply(fdefs, **kwargs)

        # --- Create merged
        mm = self.df_merge(rename=False)
        mm = mm[fnames + header]

        # --- Create validation folds
        self.create_valid_column(df=mm, folds=folds)

        # --- Join and split
        header = header + ['valid'] + list(df.columns)
        df = df.join(mm)

        # --- Create new DB() object
        db = self.new_db(prefix=prefix, subdir=subdir, fnames=df[fnames], header=df[header], rewrite=True)
        db.to_yml()

        # --- Final output
        printd('Summary complete: %i patients | %i slices' % (mm.shape[0], df.shape[0]))

        return db

    def create_valid_column(self, df=None, folds=5):

        if df is None:
            df = self.header

        if 'valid' in df:
            return

        v = np.arange(df.shape[0]) % folds 
        v = v[np.random.permutation(v.size)]

        df['valid'] = v

    # ===================================================================
    # EXTRACT and SERIALIZE 
    # ===================================================================

    def new_db(self, prefix, **kwargs):
        """
        Method to create new empty DB() object with same attributes as current object

        """
        kwargs.update({k: getattr(self, k) for k in self.ATTRS})
        kwargs.pop('files')

        # --- Initialize paths
        kwargs['paths'] = self.paths

        # --- Retain only sforms that match fnames
        if 'fnames' in kwargs:
            kwargs['sform'] = {k: v for k, v in kwargs['sform'].items() if k in kwargs['fnames']}

        return DB(prefix=prefix, **kwargs)

    def to_json(self, dat, lbl=None, hdr=None, prefix='local://', max_rows=None, exists_only=True):
        """
        Method to serialize contents of DB to JSON

        :return 
        
          (dict) combined = {

            [sid_00]: {

                'fnames': {
                    'dat': ..., 
                    'lbl': ...},

                'header': {
                    'sid': ...,
                    'fname': '/path/to/dat', 
                    'meta_00': ...,
                    'meta_01': ...}},

            [sid_01]: {
                'fnames': {...},  ==> from self.fnames
                'header': {...}}, ==> from self.header

            [sid_02]: {
                'fnames': {...},
                'header': {...}},
            ...

        }

        """
        # --- Prepare cols 
        cols = {dat: 'dat'} if lbl is None else {dat: 'dat', lbl: 'lbl'} 

        # --- Prepare fnames, header
        fnames = self.fnames_expand(cols=cols)
        header = self.header[hdr or self.header.columns]

        # --- Keep existing files
        if exists_only:
            mask = next(iter(self.exists(cols=[dat], verbose=False, ret=True).values()))
            fnames = fnames[mask]
            header = header[mask]

        # --- Add prefix
        for col in fnames.columns:
            fnames[col] = ['{}{}'.format(prefix, f) for f in fnames[col]]

        # --- Change names
        fnames = fnames.rename(columns=cols)

        fnames = fnames.to_dict(orient='index')
        header = header.to_dict(orient='index')

        # --- Extract sid, fname
        extract = lambda k : {'sid': k, 'fname': fnames[k]['dat']}
        header = {k: {**v, **extract(k)} for k, v in header.items()} 

        header = {k: {'header': v} for k, v in header.items()}
        fnames = {k: {'fnames': v} for k, v in fnames.items()}

        return {k: {**fnames[k], **header[k]} for k in fnames}

    def to_dict(self):
        """
        Method to create dictionary of metadata

        """
        return {attr: getattr(self, attr) for attr in self.ATTRS}

    def to_yml(self, fname=None, to_csv=True):
        """
        Method to serialize metadata of DB to YML

        """
        fname = fname or self.get_files()['yml']

        if fname is not None:
            os.makedirs(os.path.dirname(fname), exist_ok=True)
            with open(fname, 'w') as y:
                yaml.dump(self.to_dict(), y, sort_keys=False)

        if to_csv:
            self.to_csv()

    def to_csv(self, fname=None):
        """
        Method to serialize contents of DB to CSV

        """
        fname = fname or self.get_files()['csv']

        if fname is not None:

            df = self.df_merge(rename=True)
            os.makedirs(os.path.dirname(fname), exist_ok=True)
            df.to_csv(fname)

    def archive(self, cols=None, fname='./tars/data.tar', mask=None, include_db=True, include_code=True, project_id=None, compress=False):
        """
        Method to create *.tar(.gz) archive of the specified column(s)

        """
        # --- Filter to ensure all provided columns exist as fnames
        cols = cols or list(self.fnames.columns)
        for col in cols:
            assert col in self.fnames

        # --- Determine compression
        if compress:
            mode = 'w:gz'
            if fname[-2:] != 'gz':
                fname = fname + '.gz'
        else:
            mode = 'w'

        # --- Make directory
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        done = set() 

        with tarfile.open(fname, mode, dereference=True) as tf:

            if include_code:

                project_ids = []
                extract_pid = lambda fname : yaml.load(open(fname, 'r'), Loader=yaml.FullLoader)['_id']['project']

                for ext in ['yml', 'csv']:
                    root = os.path.dirname(self.get_files()[ext])
                    fnames = glob.glob('{}/*.{}*'.format(root, ext))
                    for fname in fnames:

                        if ext == 'yml':
                            # --- Confirm that project_id matchs
                            pid = extract_pid(fname)
                            project_ids.append(pid)
                            if pid == (project_id or pid): 
                                tf.add(fname, arcname=fname.replace(self.paths['code'], ''))

                        else:
                            tf.add(fname, arcname=fname.replace(self.paths['code'], ''))

                    # --- Ensure only single project_id is present
                    if ext == 'yml' and project_id is None:
                        if len(set(project_ids)) > 1:
                            printd('ERROR more than one project_id found, please specify project_id explicitly')
                            return

            elif include_db:
                for fname in self.get_files().values():
                    tf.add(fname, arcname=fname.replace(self.paths['code'], ''))

            for sid, fnames, header in self.cursor(mask=mask, drop_duplicates=True, subset=cols, status='Archiving | {:06d}'):
                for col in cols:
                    if os.path.exists(fnames[col]) and fnames[col] not in done:
                        tf.add(fnames[col], arcname=fnames[col].replace(self.paths['data'], ''))
                        done.add(fnames[col])
    
    def unarchive(self, tar, path=None):
        """
        Method to unpack *.tar(.gz) archive (and sort into appropriate folders)

        """
        path = path or self.paths['data'] or '.'
        jtools.unarchive(tar, path)
