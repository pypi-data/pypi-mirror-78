import os, glob, json, requests, tarfile
from ..general import printp, printd, tools as jtools

def download(name, project_id=None, path=None, overwrite=False):
    """
    Method to download prepared dataset

    """
    project_id = project_id or get_pids()[name]
    paths = jtools.get_paths(project_id=project_id, verbose=False)

    if not os.path.exists(paths['data']) or overwrite:

        path = path or '/data/raw/{}'.format(project_id.replace('/', '_').replace('-', '_'))
        path = os.path.abspath(path)
        retrieve(name, path, overwrite)
        paths = jtools.set_paths(path, project_id=project_id)

    return paths

def retrieve(name, path, overwrite):
    """
    Method to download remote data archive

    """
    tar = '{}/tars/data.tar'.format(path)

    # --- Download
    if not os.path.exists(tar) or overwrite:
        os.makedirs(os.path.dirname(tar), exist_ok=True)
        pull(name, tar)

    # --- Return if data was not downloaded
    if not os.path.exists(tar):
        return

    # --- Unarchive 
    if not os.path.exists('{}/proc'.format(path)) or overwrite:
        jtools.unarchive(tar, path)

def pull(name, dst):
    """
    Method to pull provided dataset name

    """
    # --- Find url for provided name
    URLS = get_urls()
    if name not in URLS:
        printd('ERROR provided dataset name is not recognized')
        return

    # --- Perform pull blocks of data from remote URL
    r = requests.get(URLS[name], stream=True)

    total_size = int(r.headers.get('content-length', 0))
    block_size = 32768
    dload_size = 0

    with open(dst, 'wb') as f:
        for data in r.iter_content(block_size):
            dload_size += len(data)
            printp('Downloading dataset to {} ({:0.3f} MB / {:0.3f} MB)'.format(
                dst, dload_size / 1e6, total_size / 1e6), dload_size / total_size)
            f.write(data)

    printp('Completed dataset download to {} ({:0.3f} MB / {:0.3f} MB)'.format(
        dst, dload_size / 1e6, total_size / 1e6), dload_size / total_size)

def get_urls(link='https://www.dropbox.com/s/4s0yqldmirsn3tc/urls.json?dl=1'):
    """
    Method to get url links 

    """
    return requests.get(link, stream=False).json()

def get_pids(link='https://www.dropbox.com/s/cwijcvvs258xuqp/pids.json?dl=1'):
    """
    Method to get project_ids 

    """
    return requests.get(link, stream=False).json()

def update_jsons(name, url, project_id, urls_json='./urls.json', pids_json='./pids.json'):
    """
    Method to create updated urls.json and pids.json objects with new archive

    """
    urls = get_urls()
    pids = get_pids()
    
    urls[name] = url
    pids[name] = project_id

    urls = {k: urls[k] for k in sorted(urls.keys())}
    pids = {k: pids[k] for k in sorted(pids.keys())}

    json.dump(urls, open(urls_json, 'w'))
    json.dump(pids, open(pids_json, 'w'))
