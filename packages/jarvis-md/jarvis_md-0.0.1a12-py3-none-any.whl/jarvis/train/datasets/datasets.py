from ...utils.datasets import download, get_pids
from ..client import Client 

def prepare(name=None, project_id=None, version_id=None, configs={}, keyword=''):
    """
    Method to create Python generators for train / valid data

    """
    project_id = project_id or get_pids()[name]

    client = Client(
        configs=configs,
        project_id=project_id,
        version_id=version_id,
        prefix='client*{}'.format(keyword))

    gen_train, gen_valid = client.create_generators()

    return gen_train, gen_valid, client
