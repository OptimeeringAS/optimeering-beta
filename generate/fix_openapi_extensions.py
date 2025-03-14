import argparse
import json
from collections import defaultdict
from enum import Enum
from typing import Any, Dict, Iterable, List, Tuple


class OptimeeringVendorExtensions(Enum):
    # Adds method to transform a class into another class
    # Component has properties that is a superset of another component
    # so it can be converted to another component
    # e.g. class A has properties a,b and c; class B has properties a and b
    # class A can be converted to class B
    # Adds `convert_to_{CLASS_WITH_SUBSET}` method
    POLYMORPHISM_DIRECT = "x-optimeering-direct-polymorphism"

    # Component is a list like object where each item has POLYMORPHISM_DIRECT extension
    # Adds method to iterate though its items and convert each item to supported component
    # Adds `convert_to_{CLASS_WITH_SUBSET}` method
    POLYMORPHISM_COMPONENT = "x-optimeering-component-polymorphism"

    # Replace documentation for API with documentation provided in this extension when generating client
    SDK_DOCSTRING = "x-optimeering-sdk-docstring"

    # Indicates that the route supports pagination
    # When generating client, the method for the route has pagination logic injected into it
    PAGINATED_ROUTES = "x-optimeering-paginated-route"

    # Indicates the parameter is used for pagination
    # When generating client, these parameters are removed from any route with PAGINATED_ROUTES extension
    PAGINATION_PARAMETER = "x-optimeering-pagination-parameter"

    # Indicates that parameter supports multiple values separated by comma
    # While generating client, the parameter type is changed to list
    COMMA_SEPARATED_PARAMETER = "x-optimeering-comma-separated"

    # Indicates that the parameter values are checked by an Enum
    # While generate openapi specs, an hyperlink to list all possible values is added to the description
    ALLOWED_PARAMETER_VALUES = "x-optimeering-allowed-parameter-values"

    # Indicates that items in the model has series id properties
    # while generating client, add `series_ids` method that returns a list of all series id
    MODELS_WITH_SERIES_ID = "x-optimeering-model-with-series-ids"

    # While generating client, adds `datapoint` method
    DATAPOINT_METHOD = "x-optimeering-datapoint-info"

    # While generating client, adds `__iter__` method, allowing iteration on the class
    ITERABLE_MODEL = "x-optimeering-iterable"

    # While generating client, overwrites typing information
    # E.g. datetime type is string for openapi specs with format `date-time`
    # which is not directly changed to py datetime. This extension can be used to overwrite the typing
    PYTHON_TYPING = "x-optimeering-bypass-py-typing"

    # Same as above; this one has more information related to python Annotations
    # TODO: check if it is possible to get rid of one
    ALTERNATE_TYPE_SUPPORTED = "x-optimeering-alternate-typing"

    # When a route has this extension, adds a decorator `silent_type_cast` over the method for the route.
    # The extension when detects Annotations with Union in args/kwargs typing,
    # attempts to convert the value to the first type defined in the Union using the method generated
    # by POLYMORPHISM extension.
    ROUTE_SUPPORTS_ALTERNATE_TYPE_SUPPORTED = "x-optimeering-route-supports-alternate-datatypes"

    # Denotes that the value field has complex data structure
    # When generating client, adds `unpack_value_method` to `to_pandas` method
    COMPLEX_VALUE_IN_MODEL = "x-optimeering-complex-value"


def replace_sdk_docstring(openapi_spec: Dict):
    for _, path_description in openapi_spec["paths"].items():
        for _, method_description in path_description.items():
            sdk_doc_string = method_description.get(OptimeeringVendorExtensions.SDK_DOCSTRING.value)
            if sdk_doc_string:
                method_description["description"] = sdk_doc_string

    for _, schema_value in openapi_spec["components"]["schemas"].items():
        sdk_doc_string = schema_value.get(OptimeeringVendorExtensions.SDK_DOCSTRING.value)
        if sdk_doc_string:
            schema_value["description"] = sdk_doc_string


def remove_and_replace_referenced_enums_in_component(openapi_specs: Dict):
    """
    Replace all enum references with type defination
    :param openapi_specs:
    :return:
    """
    enum_reference_collection: Dict[str, List[Tuple]] = defaultdict(list)

    # build references to enum components
    for component_name, component_definition in openapi_specs["components"]["schemas"].items():
        if component_name.startswith("Enum") and "enum" in component_definition:
            continue
        for property_name, property_definition in component_definition.get("properties", {}).items():
            if property_definition.get("$ref", "").startswith("#/components/schemas/Enum"):
                enum_component_name = property_definition["$ref"].replace("#/components/schemas/", "")
                enum_reference_collection[enum_component_name].append((component_name, property_name, None, None))
            else:
                for descriptor_type in ("allOf", "anyOf"):
                    multi_schema = property_definition.get(descriptor_type, {})
                    for ref_idx, ref_def in enumerate(multi_schema):
                        if ref_def.get("$ref", "").startswith("#/components/schemas/Enum"):
                            enum_component_name = ref_def.get("$ref", "").replace("#/components/schemas/", "")
                            enum_reference_collection[enum_component_name].append(
                                (component_name, property_name, descriptor_type, ref_idx)
                            )
    # Filter the `enum_reference_collection` to ensure only actual enums are passed
    enum_reference_collection = {
        k: v for k, v in enum_reference_collection.items() if "enum" in openapi_specs["components"]["schemas"][k]
    }

    # replace reference to enum components
    for enum_component_name, enum_references in enum_reference_collection.items():
        component_info = openapi_specs["components"]["schemas"][enum_component_name]
        title = component_info["title"]
        origin_type = component_info["type"]
        del component_info["enum"]
        for enum_ref in enum_references:
            replace_comp_name, property_name, descriptor_type, descriptor_idx = enum_ref
            openapi_specs["components"]["schemas"][replace_comp_name]["properties"][property_name]["title"] = title

            if descriptor_type is None:
                # any of and all of not found
                # ref found instead # delete ref
                replace_schemas = openapi_specs["components"]["schemas"][replace_comp_name]["properties"][property_name]
                del replace_schemas["$ref"]
                # add ref from component type
                replace_schemas["type"] = origin_type
                continue

            replace_schemas = openapi_specs["components"]["schemas"][replace_comp_name]["properties"][property_name][
                descriptor_type
            ]
            if len(replace_schemas) == 1:
                # If any of and all of is only one item delete the list reference
                # and directly assign the origin type
                del openapi_specs["components"]["schemas"][replace_comp_name]["properties"][property_name][
                    descriptor_type
                ]
                openapi_specs["components"]["schemas"][replace_comp_name]["properties"][property_name][
                    "type"
                ] = origin_type
            else:
                # Delete reference and set type from the component
                del replace_schemas[descriptor_idx]["$ref"]
                replace_schemas[descriptor_idx]["type"] = origin_type


def remove_comma_separated_docs(openapi_spec: Dict):
    """Remove documentation for comma separated parameters."""
    for _, path_definition in openapi_spec["paths"].items():
        for method, method_definition in path_definition.items():
            if method != "get":
                continue
            for parameter_definition in method_definition.get("parameters", []):
                if OptimeeringVendorExtensions.COMMA_SEPARATED_PARAMETER.value in parameter_definition.get(
                    "schema", {}
                ):
                    comma_doc = " Multiple values can be specified by separating with a comma."
                    if "description" in parameter_definition:
                        parameter_definition["description"] = parameter_definition["description"].replace(comma_doc, "")
                    if "description" in parameter_definition.get("schema", {}):
                        parameter_definition["schema"]["description"] = parameter_definition["schema"][
                            "description"
                        ].replace(comma_doc, "")


def remove_hyperlinks_from_docs(openapi_spec: Dict):
    """Remove hyper links for allowed values in documentation"""
    for path, path_definition in openapi_spec["paths"].items():
        _, _, api_name, _ = path.split("/", 3)
        for method, method_definition in path_definition.items():
            if method != "get":
                continue
            for parameter_definition in method_definition.get("parameters", []):
                if OptimeeringVendorExtensions.ALLOWED_PARAMETER_VALUES.value in parameter_definition.get("schema", {}):
                    hyperlink_doc = f" List of available values [here](/api/{api_name}/parameters/{parameter_definition['schema'][OptimeeringVendorExtensions.ALLOWED_PARAMETER_VALUES.value]['parameter-name']})."
                    if "description" in parameter_definition:
                        parameter_definition["description"] = parameter_definition["description"].replace(
                            hyperlink_doc, ""
                        )
                    if "description" in parameter_definition.get("schema", {}):
                        parameter_definition["schema"]["description"] = parameter_definition["schema"][
                            "description"
                        ].replace(hyperlink_doc, "")


def move_optimeering_extensions_out_of_schema(content):
    """
    Logic for moving extension out of schema
    """
    for _, methods in content["paths"].items():
        for _, method_definition in methods.items():
            parameters = method_definition.get("parameters", [])
            for parameter in parameters:
                if "schema" not in parameter:
                    continue
                for key in list(parameter["schema"]):
                    if key.startswith("x-"):
                        parameter[key] = parameter["schema"].pop(key)
            body_schema = (
                method_definition.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
            )
            if body_schema:
                extensions = {k: v for k, v in body_schema.items() if k.startswith("x-")}
                method_definition["requestBody"] = {**method_definition["requestBody"], **extensions}


def fix_openapi_extensions(schema_path: str) -> None:
    with open(schema_path, "r") as file:
        content = json.load(file)

    replace_sdk_docstring(content)
    remove_comma_separated_docs(content)
    remove_hyperlinks_from_docs(content)
    remove_and_replace_referenced_enums_in_component(content)
    remove_parameter_enums(content)

    move_optimeering_extensions_out_of_schema(content)
    filter_schema_components(content)

    print(json.dumps(content, indent=4, sort_keys=True))


def remove_parameter_enums(openapi_doc: Dict):
    for path, path_description in openapi_doc["paths"].items():
        try:
            _, api, app_name, route, _ = path.split("/", 4)
        except ValueError:
            continue
        if api == "api" and route == "parameters":
            for _, method_description in path_description.items():
                for param_description in method_description.get("parameters", []):
                    expected_enum_name = f"Enum{app_name.capitalize()}Parameters"
                    component_reference = param_description.get("schema", {}).get("$ref")
                    if component_reference == f"#/components/schemas/{expected_enum_name}":
                        enum_component_type = openapi_doc["components"]["schemas"][expected_enum_name]["type"]
                        del openapi_doc["components"]["schemas"][expected_enum_name]
                        del param_description["schema"]["$ref"]
                        param_description["schema"]["type"] = enum_component_type


def resolve_schema_ref_in_schema(schema_components: Dict, schema_name_list: List[str]):
    """
    Fetches all the schema references in schemas with name provided in schema_name_list

    :param schema_components:
    :param schema_name_list:
    :return:
    """
    final_schema = {}
    for schema in schema_name_list:
        final_schema[schema] = schema_components[schema]
        newly_discovered_schema = recursively_get_ref(schema_components[schema])
        final_schema = {**final_schema, **resolve_schema_ref_in_schema(schema_components, newly_discovered_schema)}
    return final_schema


def filter_schema_components(complete_schema: Dict) -> Dict:
    """
    Filters schema components based on the schemas in route
    :param complete_schema:
    :return:
    """
    schema_ref_in_path = recursively_get_ref(complete_schema["paths"])
    final_schema = resolve_schema_ref_in_schema(
        schema_components=complete_schema["components"]["schemas"], schema_name_list=schema_ref_in_path
    )
    complete_schema["components"]["schemas"] = final_schema
    return complete_schema


def recursively_get_ref(dictionary: Any) -> List[str]:
    """
    Returns all the schema name references in the dictionary

    :param dictionary:
    :return:
    """
    ref_collection = []
    if isinstance(dictionary, Dict):
        for key, value in dictionary.items():
            if key == "$ref":
                schema_name = value.replace("#/components/schemas/", "")
                ref_collection.append(schema_name)
            else:
                ref_collection.extend(recursively_get_ref(value))
    elif isinstance(dictionary, str):
        return ref_collection
    elif isinstance(dictionary, Iterable):
        for item in dictionary:
            ref_collection.extend(recursively_get_ref(item))
    return ref_collection


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-s", "--Schema", help="OpenAPI Schema file")

    # Read arguments from command line
    args = parser.parse_args()

    if args.Schema:
        fix_openapi_extensions(args.Schema)
    else:
        raise FileNotFoundError
