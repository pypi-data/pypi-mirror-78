import json
from abc import abstractmethod
from collections import defaultdict

from azureml.designer.serving.dagengine.constants import COLUMN_ATTRIBUTES_KEY
from azureml.designer.serving.dagengine.utils import decode_nan
from azureml.designer.serving.dagengine.score_exceptions import InputDataError
from azureml.studio.core.logger import get_logger, TimeProfile
from azureml.studio.core.utils.dictutils import get_value_by_key_path

logger = get_logger(__name__)


class BaseProcessor(object):
    def run(self, raw_data):
        with TimeProfile('Pre-processing'):
            try:
                webservice_input, global_parameters = self.pre_process(raw_data)
            except Exception as ex:
                logger.error(f'Run: Pre-processing error: {ex}')
                raise InputDataError(self.dag.input_schemas, raw_data)

        with TimeProfile('Processing'):
            webservice_output, name2schema = self.dag.execute(webservice_input, global_parameters)

        with TimeProfile('Post-processing'):
            response_json = self.post_process(webservice_output, name2schema)

        return response_json

    @abstractmethod
    def pre_process(self, raw_data):
        pass

    @abstractmethod
    def post_process(self, output_name2data, name2schema):
        pass


class NewProcessor(BaseProcessor):
    def __init__(self, dag):
        self.dag = dag

    def pre_process(self, raw_data):
        json_data = json.loads(raw_data)
        all_inputs = json_data['Inputs']
        webservice_input = {}
        for input_name, input_data in all_inputs.items():
            input_entry = defaultdict(list)
            for row in input_data:
                for key, val in row.items():
                    input_entry[key].append(decode_nan(val))
            webservice_input[input_name] = input_entry
        global_parameters = json_data.get('GlobalParameters', {})
        if not global_parameters:
            global_parameters = {}
        return webservice_input, global_parameters

    def post_process(self, output_name2data, name2schema):
        result = {'Results': output_name2data}
        if not name2schema:
            logger.warning("name2schema is None, no post process on data applied")
            return result
        # Convert image bytes to base64 datauri
        for output_name, schema in name2schema.items():
            if output_name not in output_name2data:
                logger.warning(f"output_name {output_name} exists in schema but not in data")
                continue
            data = output_name2data[output_name]
            for column_attribute in schema.get(COLUMN_ATTRIBUTES_KEY, []):
                if not get_value_by_key_path(column_attribute, 'type') == 'Bytes':
                    continue
                mime_type = get_value_by_key_path(column_attribute, 'properties/mime_type')
                if str(mime_type).startswith('image/'):
                    image_column_name = get_value_by_key_path(column_attribute, 'name')
                    if not image_column_name:
                        logger.warning(f"columnAttribute {column_attribute} of {output_name} has no name.")
                        continue
                    for row in data:
                        if image_column_name in row:
                            row[image_column_name] = f'data:{mime_type};base64,{row[image_column_name]}'
        return result


class ClassicProcessor(BaseProcessor):
    def __init__(self, dag, with_details=True):
        self.dag = dag
        self.with_details = with_details

    def pre_process(self, raw_data):
        json_data = json.loads(raw_data)
        all_inputs = json_data['Inputs']
        webservice_input = {}
        for input_name, input_data in all_inputs.items():
            columns = input_data['ColumnNames']
            values = input_data['Values']

            input_entry = defaultdict(list)
            for i in range(len(values)):
                for idx, col in enumerate(columns):
                    input_entry[col].append(decode_nan(values[i][idx]))
            webservice_input[input_name] = input_entry
        global_parameters = json_data.get('GlobalParameters', {})
        if not global_parameters:
            global_parameters = {}
        return webservice_input, global_parameters

    def post_process(self, output_name2data, name2schema):
        response_json = {}
        for output_name, data in output_name2data.items():
            is_list = data and isinstance(data, dict) and all([isinstance(entry, list) for entry in data.values()])
            output_schema = self.name2schema[output_name]
            values = []

            if is_list:
                amount = min([len(entry) for entry in data.values()])
                if output_schema and output_schema.get_column_names():
                    values = [[data[col][i] for col in output_schema.get_column_names()]
                              for i in range(amount)]
                    column_names = output_schema.get_column_names()
                    column_types = output_schema.get_column_types()
                else:
                    values = [[data[col][i] for col in data.keys()]
                              for i in range(amount)]
                    column_names = list(data.keys())
                    column_types = []
            else:
                if output_schema and output_schema.get_column_names():
                    values = [[data[col]
                               for col in output_schema.get_column_names()]]
                    column_names = output_schema.get_column_names()
                    column_types = output_schema.get_column_types()
                else:
                    values = [[data[col] for col in data.keys()]]
                    column_names = list(data.keys())
                    column_types = []
            if self.with_details:
                response_json[output_name] = {
                    'type': 'DataTable',
                    'value': {
                        'ColumnNames': column_names,
                        'ColumnTypes': column_types,
                        'Values': values}}
            else:
                response_json[output_name] = {
                    'type': 'DataTable',
                    'value': {
                        'ColumnNames': column_names,
                        'Values': values}}
        return response_json
