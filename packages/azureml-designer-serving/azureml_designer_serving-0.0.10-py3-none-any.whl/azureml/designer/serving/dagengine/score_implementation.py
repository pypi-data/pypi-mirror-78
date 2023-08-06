import os
import importlib
import json
import pandas as pd
import subprocess
from pathlib import Path

from azureml.core.model import Model
from azureml.designer.serving.dagengine.request_handler import enable_rawhttp, handle_request, handle_not_supported
from azureml.designer.serving.dagengine.constants import DS_CONFIG_FILE_NAME, DS_PATH_ENV_VAR_NAME, \
    EXTRACTED_MODEL_DIRECTORY_NAME, MODEL_PARENT_PATH_ENV_VAR_NAME
from azureml.designer.serving.dagengine.dag import Dag
from azureml.studio.core.logger import get_logger

# Disable pandas warning when there's potential chained_assignment, because pandas would log every time it encounters
# the possibility of chained assignment and flood the AzureML service's log with this warning.
# More details available in https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.set_option.html
pd.set_option('mode.chained_assignment', None)
logger = get_logger(__name__)
graph = None


def _get_model_package_path():
    root_path = Path(os.environ.get(DS_PATH_ENV_VAR_NAME, ''))
    config_file_path = root_path / DS_CONFIG_FILE_NAME
    with open(config_file_path) as fp:
        config = json.load(fp)
        # TODO: Explicitly record model version in config file
        model_file_name = config['model']
        if ':' in model_file_name:
            model_name, version = model_file_name.rsplit(':', 1)
            version = int(version) if version.isdigit() else None
        else:
            model_name, version = model_file_name, None
        logger.info(f'Model: name={model_name}, version={version}')
    if MODEL_PARENT_PATH_ENV_VAR_NAME in os.environ:  # for local debug only
        return Path(os.environ[MODEL_PARENT_PATH_ENV_VAR_NAME]) / model_file_name
    else:
        return Path(Model.get_model_path(model_name, version))


def _load_graph():
    try:
        root_path = Path(os.environ.get(DS_PATH_ENV_VAR_NAME, ''))
        extract_to_path = root_path / EXTRACTED_MODEL_DIRECTORY_NAME
        model_package_path = _get_model_package_path()
        dag = Dag.load(model_package_path, extract_to_path)
        logger.info('Init: Graph has been loaded')
    except Exception as ex:
        logger.error(f'Init: Service init failed: {ex}')
        raise ex
    return dag


def _log_pip_freeze():
    result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    logger.info(f'pip freeze result:\n{result.stdout}')


def _reload_werkzeug():
    """Reload werkzeug package which is imported before the installation of azureml-designer-serving, thus making the
    compatibility fix done by azureml-deisnger-serving's dependency installation (azureml-defaults, to be specific)
    uneffective unless reloaded.
    """
    try:
        logger.info('Trying to reload werkzeug.')
        import werkzeug
        importlib.reload(werkzeug)
        logger.info('Successfully reloaded werkzeug.')
    except BaseException:
        logger.warning('Failed to reload werkzeug.', exc_info=True)


def init():
    _reload_werkzeug()
    _log_pip_freeze()
    global graph
    graph = _load_graph()
    enable_rawhttp()


def run(request):
    if request.method == 'POST':
        graph.clear_dynamic_data()
        return handle_request(graph, request.get_data(), request.args)
    else:
        return handle_not_supported(request)
