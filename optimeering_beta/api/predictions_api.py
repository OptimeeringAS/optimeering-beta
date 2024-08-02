# coding: utf-8

"""
    Optimeering

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

from typing import Any, Dict, List, Optional, Tuple, Union

from optimeering_beta.api_client import OptimeeringClient, RequestSerialized
from optimeering_beta.models.preds_data_get_response import PredsDataGetResponse
from optimeering_beta.models.preds_series_get_response import PredsSeriesGetResponse
from pydantic import Field, StrictFloat, StrictInt, StrictStr, validate_call
from typing_extensions import Annotated


class PredictionsApi:
    """
    Collection of methods to interact with PredictionsApi
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = OptimeeringClient.get_default()
        self.api_client = api_client

    @validate_call
    def get_prediction_series(
        self,
        name: Annotated[
            Optional[List[StrictStr]],
            Field(description="Name of the series to retrieve. If not specified, will return all series."),
        ] = None,
        area: Annotated[
            Optional[List[StrictStr]],
            Field(description="The name of the area (eg - NO3, SE4, or FI). If not specified, will return all areas."),
        ] = None,
        market: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="The market for which series should be retrieved. If not specified, will return series for all markets."
            ),
        ] = None,
        statistic: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="Statistic type (eg. 'size', 'direction', or 'quantile'). If not specified, will return series for all statistic types."
            ),
        ] = None,
        id: Annotated[
            Optional[List[StrictInt]],
            Field(description="ID of the series to retrieve. If not specified, will return all series."),
        ] = None,
        unit_type: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="Unit type (eq. 'volumes', 'price', or 'price_spread'). If not specified, will return series for all unit types."
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]],
        ] = None,
    ) -> PredsSeriesGetResponse:
        """Get Series

        Returns the prediction series

        :param name: Name of the series to retrieve. If not specified, will return all series.
        :type name: List[StrictStr]
        :param area: The name of the area (eg - NO3, SE4, or FI). If not specified, will return all areas.
        :type area: List[StrictStr]
        :param market: The market for which series should be retrieved. If not specified, will return series for all markets.
        :type market: List[StrictStr]
        :param statistic: Statistic type (eg. 'size', 'direction', or 'quantile'). If not specified, will return series for all statistic types.
        :type statistic: List[StrictStr]
        :param id: ID of the series to retrieve. If not specified, will return all series.
        :type id: List[StrictInt]
        :param unit_type: Unit type (eq. 'volumes', 'price', or 'price_spread'). If not specified, will return series for all unit types.
        :type unit_type: List[StrictStr]
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :return: Returns the result object.

        :Example:

        >>> from optimeering_beta import Configuration, OptimeeringClient
        >>> configuration = Configuration(host="https://beta.optimeering.com/api")
        >>> client = OptimeeringClient(configuration=configuration)
        >>> # Get filtered data point - replace ... with appropriate filters documented above
        >>> response = client.predictions_api.get_prediction_series(...)

        """  # noqa: E501

        _param = self._get_prediction_series_serialize(
            name=name,
            area=area,
            market=market,
            statistic=statistic,
            id=id,
            unit_type=unit_type,
            limit=None,
            offset=None,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "PredsSeriesGetResponse",
            "422": "HTTPValidationError",
        }
        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        response_data.read()
        paginated_response = self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data
        if type(paginated_response) != dict:
            paginated_response._client = self.api_client
        next_page = paginated_response.next_page

        if next_page is None:
            return paginated_response

        # resolve extendable attribute
        attribute_to_extend_selected: Optional[str] = None
        if "series_id" in set(paginated_response.items[0].model_fields):
            extendable_attribute = {"datapoints", "events"}
            attribute_to_extend = extendable_attribute.intersection(set(paginated_response.items[0].model_fields))
            if len(attribute_to_extend) == 1:
                attribute_to_extend_selected = list(attribute_to_extend)[0]
            else:
                raise AttributeError("Failed to resolve extendable attribute.")

        while next_page is not None:
            # Item at index#1 is URL, we overwrite the item with url in next_page
            next_param = tuple(value if idx != 1 else next_page for idx, value in enumerate(_param))
            next_pagination = self.api_client.call_api(*next_param, _request_timeout=_request_timeout)
            next_pagination.read()
            next_pagination = self.api_client.response_deserialize(
                response_data=next_pagination,
                response_types_map=_response_types_map,
            ).data
            next_page = next_pagination.next_page

            if attribute_to_extend_selected:
                if next_pagination.items[0].series_id == paginated_response.items[-1].series_id:
                    # if series id is same, extract the first item and extend to last item
                    continued_data: List = getattr(next_pagination.items.pop(0), attribute_to_extend_selected)
                    previous_data: List = getattr(paginated_response.items[-1], attribute_to_extend_selected)
                    previous_data.extend(continued_data)
            paginated_response.items.extend(next_pagination.items)
        return paginated_response

    def _get_prediction_series_serialize(
        self,
        name,
        area,
        market,
        statistic,
        id,
        unit_type,
        limit,
        offset,
    ) -> RequestSerialized:
        _collection_formats: Dict[str, str] = {}

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        if name is not None:
            name = ",".join(str(i) for i in name)
            _query_params.append(("name", name))

        if area is not None:
            area = ",".join(str(i) for i in area)
            _query_params.append(("area", area))

        if market is not None:
            market = ",".join(str(i) for i in market)
            _query_params.append(("market", market))

        if statistic is not None:
            statistic = ",".join(str(i) for i in statistic)
            _query_params.append(("statistic", statistic))

        if id is not None:
            id = ",".join(str(i) for i in id)
            _query_params.append(("id", id))

        if unit_type is not None:
            unit_type = ",".join(str(i) for i in unit_type)
            _query_params.append(("unit_type", unit_type))

        if limit is not None:
            _query_params.append(("limit", limit))

        if offset is not None:
            _query_params.append(("offset", offset))

        # process the header parameters
        # process the form parameters
        # process the body parameter

        # inject azure token
        _header_params["Authorization"] = f"Bearer {self.api_client.token}"

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/api/predictions/series/",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            collection_formats=_collection_formats,
        )

    @validate_call
    def get_predictions(
        self,
        series_id: Annotated[
            Optional[List[StrictInt]],
            Field(description="Series ID to filter. If not specified, will return all series."),
        ] = None,
        start: Annotated[
            Optional[Any],
            Field(
                description="The first datetime to fetch (inclusive). Defaults to current time. Should be specified in ISO 8601 datetime or duration format (eg - '2024-05-15T06:00:00+00:00', 'P1H', '-P1W1D', etc.)"
            ),
        ] = None,
        end: Annotated[
            Optional[Any],
            Field(
                description="The last datetime to fetch (exclusive). Defaults to 2099-12-30. Should be specified in ISO 8601 datetime or duration format (eg - '2024-05-15T06:00:00+00:00', 'P1H', '-P1W1D', etc.)"
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]],
        ] = None,
    ) -> PredsDataGetResponse:
        """Get Predictions

        Returns predictions

        :param series_id: Series ID to filter. If not specified, will return all series.
        :type series_id: List[StrictInt]
        :param start: The first datetime to fetch (inclusive). Defaults to current time. Should be specified in ISO 8601 datetime or duration format (eg - '2024-05-15T06:00:00+00:00', 'P1H', '-P1W1D', etc.)
        :type start: Start
        :param end: The last datetime to fetch (exclusive). Defaults to 2099-12-30. Should be specified in ISO 8601 datetime or duration format (eg - '2024-05-15T06:00:00+00:00', 'P1H', '-P1W1D', etc.)
        :type end: End
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :return: Returns the result object.

        :Example:

        >>> from optimeering_beta import Configuration, OptimeeringClient
        >>> configuration = Configuration(host="https://beta.optimeering.com/api")
        >>> client = OptimeeringClient(configuration=configuration)
        >>> # Get filtered data point - replace ... with appropriate filters documented above
        >>> response = client.predictions_api.get_predictions(...)

        """  # noqa: E501

        _param = self._get_predictions_serialize(
            series_id=series_id,
            start=start,
            end=end,
            limit=None,
            offset=None,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "PredsDataGetResponse",
            "422": "HTTPValidationError",
        }
        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        response_data.read()
        paginated_response = self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data
        if type(paginated_response) != dict:
            paginated_response._client = self.api_client
        next_page = paginated_response.next_page

        if next_page is None:
            return paginated_response

        # resolve extendable attribute
        attribute_to_extend_selected: Optional[str] = None
        if "series_id" in set(paginated_response.items[0].model_fields):
            extendable_attribute = {"datapoints", "events"}
            attribute_to_extend = extendable_attribute.intersection(set(paginated_response.items[0].model_fields))
            if len(attribute_to_extend) == 1:
                attribute_to_extend_selected = list(attribute_to_extend)[0]
            else:
                raise AttributeError("Failed to resolve extendable attribute.")

        while next_page is not None:
            # Item at index#1 is URL, we overwrite the item with url in next_page
            next_param = tuple(value if idx != 1 else next_page for idx, value in enumerate(_param))
            next_pagination = self.api_client.call_api(*next_param, _request_timeout=_request_timeout)
            next_pagination.read()
            next_pagination = self.api_client.response_deserialize(
                response_data=next_pagination,
                response_types_map=_response_types_map,
            ).data
            next_page = next_pagination.next_page

            if attribute_to_extend_selected:
                if next_pagination.items[0].series_id == paginated_response.items[-1].series_id:
                    # if series id is same, extract the first item and extend to last item
                    continued_data: List = getattr(next_pagination.items.pop(0), attribute_to_extend_selected)
                    previous_data: List = getattr(paginated_response.items[-1], attribute_to_extend_selected)
                    previous_data.extend(continued_data)
            paginated_response.items.extend(next_pagination.items)
        return paginated_response

    def _get_predictions_serialize(
        self,
        series_id,
        start,
        end,
        limit,
        offset,
    ) -> RequestSerialized:
        _collection_formats: Dict[str, str] = {}

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        if series_id is not None:
            series_id = ",".join(str(i) for i in series_id)
            _query_params.append(("series_id", series_id))

        if start is not None:
            _query_params.append(("start", start))

        if end is not None:
            _query_params.append(("end", end))

        if limit is not None:
            _query_params.append(("limit", limit))

        if offset is not None:
            _query_params.append(("offset", offset))

        # process the header parameters
        # process the form parameters
        # process the body parameter

        # inject azure token
        _header_params["Authorization"] = f"Bearer {self.api_client.token}"

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/api/predictions/",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            collection_formats=_collection_formats,
        )
