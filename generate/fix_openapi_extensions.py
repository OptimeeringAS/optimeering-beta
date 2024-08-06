import argparse
import json
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Tuple


def inject_optimeering_extensions_into_models(openapi_schema: Dict) -> None:
    """
    Injects series id method support into POST response object
    Injects reference to datapoint API into POST response object

    :param openapi_schema:
    :return:
    """
    for path, path_description in openapi_schema["paths"].items():
        is_series_response_model = path.endswith("/series/")
        for method in path_description:
            tags = path_description[method]["tags"]
            if len(tags) == 1:
                api_name = f"{tags[0].capitalize()}Api"
            else:
                raise AttributeError("API route has multiple tags.")
            response_component_name = (
                path_description[method]["responses"]["200"]["content"]["application/json"]["schema"]
                .get("$ref", "")
                .replace("#/components/schemas/", "")
            )
            if not response_component_name:
                continue
            component_reference = openapi_schema["components"]["schemas"][response_component_name]

            if is_series_response_model:
                # inject get_series_ids
                component_reference["x-optimeering-model-with-series-ids"] = {
                    "description": "This extension denotes that the response have series ids.",
                    "value": True,
                }
                # inject observations operation id and data model
                datapoint_description = openapi_schema["paths"][path[0 : -len("/series")]]["get"]
                datapoint_operation_id = datapoint_description["operationId"]
                datapoint_model = datapoint_description["responses"]["200"]["content"]["application/json"]["schema"][
                    "$ref"
                ].replace("#/components/schemas/", "")
                component_reference["x-optimeering-datapoint-info"] = {
                    "description": "This extension links responses of series API routes "
                    "to the API routes that return their datapoints.",
                    "operation-id": datapoint_operation_id,
                    "response-model-name": datapoint_model,
                    "api-name": api_name,
                }
            # Inject iterable functionality
            component_reference["x-optimeering-iterable"] = {
                "description": "This extension denotes that the response is iterable.",
                "value": True,
            }


def remove_enums_from_specs(openapi_specs: Dict):
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
                del replace_schemas[descriptor_idx]["$ref"]
                replace_schemas[descriptor_idx]["type"] = origin_type


def remove_comma_separated_docs(openapi_spec: Dict):
    """Remove documentation for comma separated parameters."""
    for _, path_definition in openapi_spec["paths"].items():
        for method, method_definition in path_definition.items():
            if method != "get":
                continue
            for parameter_definition in method_definition.get("parameters", []):
                if "x-optimeering-comma-separated" in parameter_definition.get("schema", {}):
                    comma_doc = " Multiple values can be specified by separating with a comma."
                    if "description" in parameter_definition:
                        parameter_definition["description"] = parameter_definition["description"].replace(comma_doc, "")
                    if "description" in parameter_definition.get("schema", {}):
                        parameter_definition["schema"]["description"] = parameter_definition["schema"][
                            "description"
                        ].replace(comma_doc, "")


def remove_hyperlinks_from_docs(openapi_spec: Dict):
    """Remove hyper links for allowed values in documentation"""
    for _, path_definition in openapi_spec["paths"].items():
        for method, method_definition in path_definition.items():
            if method != "get":
                continue
            for parameter_definition in method_definition.get("parameters", []):
                if "x-optimeering-allowed-parameter-values" in parameter_definition.get("schema", {}):
                    hyperlink_doc = f" List of available values [here](/api/parameters/{parameter_definition['schema']['x-optimeering-allowed-parameter-values']['parameter-name']})."
                    if "description" in parameter_definition:
                        parameter_definition["description"] = parameter_definition["description"].replace(
                            hyperlink_doc, ""
                        )
                    if "description" in parameter_definition.get("schema", {}):
                        parameter_definition["schema"]["description"] = parameter_definition["schema"][
                            "description"
                        ].replace(hyperlink_doc, "")


def fix_openapi_extensions(schema_path: str) -> None:
    with open(schema_path, "r") as file:
        content = json.load(file)
    remove_comma_separated_docs(content)
    remove_hyperlinks_from_docs(content)
    remove_enums_from_specs(content)
    for _, methods in content["paths"].items():
        for _, method_definition in methods.items():
            if "parameters" not in method_definition:
                continue
            parameters = method_definition["parameters"]
            for parameter in parameters:
                if "schema" not in parameter:
                    continue
                for key in list(parameter["schema"]):
                    if key.startswith("x-"):
                        parameter[key] = parameter["schema"].pop(key)
    filter_schema_components(content)
    inject_optimeering_extensions_into_models(content)

    print(json.dumps(content, indent=4, sort_keys=True))


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
        print(json.dumps({"error": f"No file present at {args.Schema}"}))
