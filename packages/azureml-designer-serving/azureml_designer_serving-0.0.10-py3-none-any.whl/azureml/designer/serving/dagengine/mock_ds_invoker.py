import os
import pandas as pd

from azureml.studio.core.utils.yamlutils import load_yaml_file
from azureml.studio.core.io.any_directory import AnyDirectory
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.studio.core.io.model_directory import ModelDirectory
from azureml.designer.serving.dagengine.module_host import StandardCustomModuleHost


PORT_TYPES = {
    'ModelDirectory',
    'DataFrameDirectory',
    'TransformationDirectory',
    'ImageDirectory',
}

STATIC_PORT_TYPES = {
    'ModelDirectory',
    'TransformationDirectory',
}


def is_static_port_type(port_type):
    return port_type in STATIC_PORT_TYPES


class MockModule:
    def run(self, model, data_frame, optional_data_frame, arg, sub_arg):
        return model, data_frame

    def on_init(self, *args, **kwargs):
        pass


def flattern_input_definitions(input_definitions):
    results = []
    for input_definition in input_definitions:
        results.append(input_definition)
        if 'options' in input_definition:
            for option in input_definition['options']:
                if isinstance(option, dict):
                    results += flattern_input_definitions(next(value for value in option.values()))
    return results


def parse_port(port_type, raw_value):
    if raw_value is None:
        return None
    if isinstance(raw_value, AnyDirectory):
        return raw_value
    if isinstance(raw_value, (str, os.PathLike)):
        return AnyDirectory.load_dynamic(raw_value)
    if isinstance(raw_value, pd.DataFrame):
        return DataFrameDirectory.create(data=raw_value)
    elif port_type == 'ModelDirectory':
        return ModelDirectory.create(model=raw_value)
    raise ValueError(f"raw_value cannot be parsed as type {port_type}")


def get_inputs_and_params(input_definitions, kwargs):
    static_inputs = {}
    dynamic_inputs = {}
    params = {}
    input_definitions = flattern_input_definitions(input_definitions)
    for input_definition in input_definitions:
        input_name = input_definition['name']
        input_type = input_definition.get('type')
        raw_value = kwargs.pop(input_name) if input_name in kwargs else None
        if input_type in PORT_TYPES:
            port = parse_port(input_type, raw_value)
            if port is not None and port.TYPE_NAME != input_type:
                raise ValueError(
                    f"Input port '{input_name}' type mismatch, expect '{input_type}', got '{port.TYPE_NAME}'."
                )
            if is_static_port_type(input_type):
                static_inputs[input_name] = port
            else:
                dynamic_inputs[input_name] = port
        else:
            params[input_name] = raw_value
    if len(kwargs) > 0:
        raise KeyError(f"The following args are not in module spec: {', '.join(kwargs)}.")
    return static_inputs, dynamic_inputs, params


def get_invoking_class_name(spec):
    implementation = spec['implementation']
    entry = implementation.get('invoking') or implementation.get('servingEntry')
    if entry is None:
        raise ValueError("Serving entry is not provided.")
    return entry['module'], entry['class']


def validate_outputs(output_definitions, outputs):
    if len(outputs) != len(output_definitions):
        raise Exception(f"Output count incorrect, expect {len(output_definitions)}, got {len(outputs)}")
    for definition, output in zip(output_definitions, outputs):
        def_type = definition['type']
        output_type = output.TYPE_NAME if isinstance(output, AnyDirectory) else type(output).__name__
        if def_type != output_type:
            raise Exception(f"Output {definition['name']} type incorrect, expect {def_type}, got {output_type}")


def invoke_like_ds(spec_or_yaml_file, kwargs):
    spec = spec_or_yaml_file if isinstance(spec_or_yaml_file, dict) else load_yaml_file(spec_or_yaml_file)

    static_inputs, dynamic_inputs, params = get_inputs_and_params(spec['inputs'], kwargs)
    port_names = [name for name in static_inputs] + [name for name in dynamic_inputs]
    module_name, class_name = get_invoking_class_name(spec)
    module_host = StandardCustomModuleHost(
        module_name=module_name,
        class_name=class_name,
        static_source_dict=static_inputs,
        parameters=params,
        input_port_arg_names=port_names
    )

    outputs = module_host.execute(
        dynamic_source_dict=dynamic_inputs,
        global_parameters={}
    )
    validate_outputs(spec['outputs'], outputs)
    return outputs
