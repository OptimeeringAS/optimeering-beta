# coding: utf-8

"""
    Optimeering

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

from typing import Dict, List, Optional, Tuple, Union

from optimeering_beta.api_client import OptimeeringClient, RequestSerialized
from optimeering_beta.models.enum_parameters import EnumParameters
from pydantic import Field, StrictFloat, validate_call
from typing_extensions import Annotated


class ParametersApi:
    """
    Collection of methods to interact with ParametersApi
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = OptimeeringClient.get_default()
        self.api_client = api_client

    @validate_call
    def get_parameter_values(
        self,
        param: EnumParameters,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]],
        ] = None,
    ) -> object:
        """Parameter List


        :param param: (required)
        :type param: EnumParameters
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :return: Returns the result object.
        :rtype: object

        :Example:

        >>> from optimeering_beta import Configuration, OptimeeringClient
        >>> configuration = Configuration(host="https://beta.optimeering.com")
        >>> client = OptimeeringClient(configuration=configuration)
        >>> # Post data point - replace ... with correct dataformat documented above
        >>> response = client.parameters_api.get_parameter_values(...)

        """  # noqa: E501

        _param = self._get_parameter_values_serialize(
            param=param,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "object",
            "422": "HTTPValidationError",
        }
        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        response_data.read()
        response = self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data
        if type(response) != dict:
            response._client = self.api_client
        return response

    def _get_parameter_values_serialize(
        self,
        param,
    ) -> RequestSerialized:
        _collection_formats: Dict[str, str] = {}

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if param is not None:
            _path_params["param"] = param.value
        # process the query parameters
        # process the header parameters
        # process the form parameters
        # process the body parameter

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/api/parameters/{param}",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            collection_formats=_collection_formats,
        )
