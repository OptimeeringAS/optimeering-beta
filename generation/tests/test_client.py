import inspect
import json
import unittest.mock
from unittest import TestCase

import optimeering_beta
from optimeering_beta import Configuration, OptimeeringClient
from optimeering_beta.azure_authentication import AzureAuth
from optimeering_beta.rest import RESTClientObject, RESTResponse

config = Configuration(host="Testurlhere")
client = OptimeeringClient(config)

with open("./generation/openapi.json", "r") as file:
    OPENAPI_SPEC = json.load(file)


def generate_data(model: str):
    model_def = OPENAPI_SPEC["components"]["schemas"][model]
    data = {}
    for property_name, property in model_def["properties"].items():
        if "anyOf" in property:
            property = property["anyOf"][0]
        property_type = property["type"]
        if property_type == "string":
            if property.get("format") == "date-time":
                data[property_name] = "2000-01-01T00:00:00+00:00"
                continue
            else:
                data[property_name] = "mock string"
                continue
        elif property_type == "integer":
            data[property_name] = 1
            continue
        elif property_type == "array":
            if "anyOf" in property["items"]:
                component_ref = property["items"]["anyOf"][0]["$ref"]
            else:
                component_ref = property["items"]["$ref"]
            data[property_name] = [generate_data(component_ref.split("/")[-1])]
            continue
        elif property_type == "object":
            if property.get("additionalProperties", {}).get("type") == "number":
                data[property_name] = {"mock_key": 1}
                continue

        raise TypeError(f"Unsupported type {property_type}")
    return data


class FakeResponse:
    def __init__(self, data):
        if "next_page" in data:
            data["next_page"] = None
        self.data = json.dumps(data, default=str).encode()
        self.status = 200
        self.reason = None
        self.headers = {}


class TestGeneratedClient(TestCase):
    def setUp(self):
        self.mock_azure = unittest.mock.patch.object(AzureAuth, "get_token", return_value=None)
        self.mock_azure.start()

    def tearDown(self):
        self.mock_azure.stop()

    def test_api_series_and_single_datapoint(self):
        """Tests calling series and getting one datapoint"""

        apis_to_test = {
            k: v
            for k, v in optimeering_beta.api.__dict__.items()
            if k.endswith("Api") and v.__module__.startswith("optimeering_beta.api")
        }

        for api_name in apis_to_test:
            api = getattr(optimeering_beta, api_name)(api_client=client)

            # get series
            for method in [i[0] for i in inspect.getmembers(api) if i[0].endswith("series")]:
                api_method = getattr(api, method)
                response_model_type = inspect.signature(api_method).return_annotation
                data = generate_data(response_model_type.__name__)
                with unittest.mock.patch.object(
                    RESTClientObject, "request", return_value=RESTResponse(FakeResponse(data))
                ):
                    response = api_method()
                assert len(response.items) > 0

                # get datapoints
                response_model_type = eval(inspect.signature(response.datapoints).return_annotation)

                data = generate_data(response_model_type.__name__)
                with unittest.mock.patch.object(
                    RESTClientObject, "request", return_value=RESTResponse(FakeResponse(data))
                ):
                    datapoints = response.datapoints()

                assert len(datapoints.items) == 1
