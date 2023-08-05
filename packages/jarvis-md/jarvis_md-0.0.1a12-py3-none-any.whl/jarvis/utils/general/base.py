import os, yaml
import pandas as pd
from . import tools as jtools
from .rdict import recursive_set
from .printer import printd

class Base():

    def load_configs(self, names=['jhubd']):
        """
        Method to load ~/.jarvis configuration files

        """
        self.load_env()

        for name in names:
            self.load_configs_by_name(name)

        if 'jhubd' in names:
            self.load_configs_jhubd()

        self.load_configs_custom()

    def load_env(self):
        """
        Method to load JARVIS env variables

        """
        parse = lambda x : int(x) if x.isnumeric() else x 
        self.ENV = {k[7:]: parse(v) for k, v in os.environ.items() if k[:7] == 'JARVIS_'}

    def load_configs_by_name(self, name):

        setattr(self, name, jtools.load_configs(name=name))

    def load_configs_jhubd(self):
        """
        Method to load JarvisHub daemon configs

        """
        store = self.ENV.get('HUB_STORE', None)

        if store is None:
            return

        if not hasattr(self, 'jhubd'):
            self.load_configs_by_name('jhubd')

        # --- Set JarvisHub store root
        self.jhubd['store'] = store

        # --- Set daemon paths
        for k in self.jhubd['daemons']:
            if self.jhubd['daemons'][k]['path'] is not None:
                self.jhubd['daemons'][k]['path'] = self.jhubd['daemons'][k]['path'].format(store=store)

    def load_configs_custom(self): pass

    def load_decorator(func):

        def wrapper(self, fname, *args, **kwargs):

            if os.path.exists(fname):
                return func(self, fname, *args, **kwargs)

        return wrapper

    @load_decorator
    def load_yml(self, fname, **kwargs):

        return yaml.load(open(fname, 'r'), Loader=yaml.FullLoader, **kwargs)

    @load_decorator
    def load_csv(self, fname, **kwargs):

        return pd.read_csv(fname, **kwargs)

    def save_decorator(func):

        def wrapper(self, fname, *args, **kwargs):

            os.makedirs(os.path.dirname(fname), exist_ok=True)
            return func(self, fname, *args, **kwargs)

        return wrapper

    @save_decorator
    def save_yml(self, fname, obj, combine_existing=True, sort_keys=False, **kwargs):
        """
        Method to save object as *.yml file

        :params

          (bool) combine_existing : if True, combine with existing *.yml file

        """
        if type(obj) is str:
            if os.path.exists(obj) and obj[-3:] == 'yml':
                obj = self.load_yml(fname=obj, **kwargs)

        if os.path.exists(fname) and combine_existing:
            prev = self.load_yml(fname, **kwargs)

            assert type(prev) is type(obj)

            if type(prev) is dict:
                recursive_set(prev, obj) 
                obj = prev

            elif type(prev) is list:
                prev.extend(obj)
                obj = prev

        yaml.dump(obj, open(fname, 'w'), sort_keys=sort_keys, **kwargs)

    @save_decorator
    def save_csv(self, fname, df, combine_existing=True, drop_duplicates=False, **kwargs):
        """
        Method to save DataFrame as *.csv file

        NOTE: df may be populated with either a DataFrame, dictionary or filename

        :params

          (bool) combine_existing : if True, combine with existing *.csv file

        """
        if type(df) is dict:
            df = pd.DataFrame.from_dict(df, **kwargs)

        if type(df) is str:
            df = self.load_csv(fname=df, **kwargs)

        if type(df) is not pd.DataFrame:
            return

        index_col = df.index.name if df.index.name != '' else None

        # --- Load existing
        if os.path.exists(fname) and combine_existing:
            prev = pd.read_csv(fname, index_col=index_col, **kwargs)
            df = pd.concat((prev, df))

            if drop_duplicates:
                df = df.drop_duplicates()

        df.to_csv(fname, index=index_col is not None)

    def print_env(self, prefix=''):

        printd('')
        printd('Jarvis | ENV variables')
        printd('')

        printd('  {key: <25} {url}'.format(key='ENV VAR', url='VALUE'))
        printd('  ' + '-' * 100)
        keys = sorted([k for k in self.ENV if k[:len(prefix)] == prefix])
        for key in keys:
            printd('  {key: <25} {value}'.format(key=key, value=self.ENV[key]))
        printd('  ' + '-' * 100)

        printd('')
