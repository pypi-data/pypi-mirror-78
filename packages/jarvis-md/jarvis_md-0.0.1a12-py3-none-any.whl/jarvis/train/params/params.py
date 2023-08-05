import os, pandas as pd, json
from ...utils.general import *
from ...utils.general import tools as jtools

def load(csv=None, row=0, client='client.yml', **kwargs):
    """
    Method to load CSV file with training hyperparameters

    :params

      (str) csv        : CSV file with hyperparameter values
      (int) row        : row of CSV file to load 
      (str) project_id : name of project_id if relative paths should be expanded
      (str) version_id : name of version_id if relative paths should be expanded

    Note that while any CSV file format is compatible, the following columns are recommended:

    output_dir | _client                | fold | ...
    ----------------------------------------------------
    ./exp01-0    /path/to/client.yml      0
    ./exp01-1    /path/to/client.yml      1
    ./exp01-2    /path/to/client.yml      2
    ----------------------------------------------------

    The _client row typically contains the source TEMPLATE client.yml file. If both _client
    and output_dir columns are present, then the following OUTPUT client file is inferred:

      client = '{}/{}'.format(output_dir, client)

    If this OUTPUT client file exists, the '_client' column is changed to the new OUTPUT file.

    """
    # --- Extract ENVIRON variables if present 
    csv = os.environ.get('JARVIS_PARAMS_CSV', None) or csv
    row = int(os.environ['JARVIS_PARAMS_ROW']) if 'JARVIS_PARAMS_ROW' in os.environ else row

    if csv is None:
        printd('ERROR no *.csv found')
        return

    # --- Load row
    df = pd.read_csv(csv)

    # --- Format dict
    p = json.loads(df.iloc[row].to_json())

    # --- Convert relative path names if needed
    _id = jtools.parse_ids(**kwargs)
    if _id['project'] is not None:
        paths = jtools.get_paths(_id['project'], _id['version'], alt_path=csv)
        root = paths.get('code', '')
        p = {k: v.format(root=root) if type(v) is str else v for k, v in p.items()}

        p['_id'] = _id
        p['_paths'] = paths

    # --- Convert client path
    if type(p.get('_client', None)) is str and type(p.get('output_dir', None)) is str:
        client = '{}/{}'.format(p['output_dir'], client)
        if os.path.exists(client):
            p['_client'] = client

    return p
