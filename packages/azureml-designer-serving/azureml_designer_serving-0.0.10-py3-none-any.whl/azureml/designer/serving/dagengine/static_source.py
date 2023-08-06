from pathlib import Path

from azureml.designer.serving.dagengine.graph_spec import GraphSpecStaticSource
from azureml.designer.serving.dagengine.score_exceptions import ResourceLoadingError
from azureml.studio.core.io.any_directory import AnyDirectory
from azureml.studio.core.logger import get_logger, TimeProfile

logger = get_logger(__name__)


class StaticSource(object):
    """Static resources stored in model_package"""
    def __init__(self, data):
        """Init func

        :param data:
        """
        self.data = data

    @classmethod
    def load(cls,
             graph_spec_static_source: GraphSpecStaticSource,
             artifact_path: Path):
        """Load from graph_spec StaticSource

        :param graph_spec_static_source:
        :param artifact_path:
        :return:
        """
        with TimeProfile(f'Loading static source {graph_spec_static_source.model_name}'):
            static_source_path = artifact_path / graph_spec_static_source.model_name
            try:
                if static_source_path.is_dir():
                    data = AnyDirectory.load_dynamic(static_source_path)
                elif static_source_path.is_file():
                    # ZipFile can't be handled by AnyDirectory.load_dynamic and has to be handled with InputHandler
                    # Custom module with ZipFile port is not supported in DS for now
                    logger.info(f"Try to load with InputHandler.handle_input_from_file_name")
                    from azureml.studio.modulehost.handler.port_io_handler import InputHandler
                    data = InputHandler.handle_input_from_file_name(static_source_path)
                else:
                    raise FileNotFoundError(f"{str(static_source_path)} does not exist.")
                logger.info(f"Loaded {data} from {static_source_path}.")
                return cls(data)

            except BaseException as e:
                raise ResourceLoadingError(static_source_path) from e
