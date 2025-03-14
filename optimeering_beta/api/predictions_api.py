# coding: utf-8

"""
    Optimeering

"""  # noqa: E501
from typing import Any, Dict, List, Optional, Tuple, Union

from optimeering_beta.api_client import OptimeeringClient, RequestSerialized
from optimeering_beta.logger import log_function_timing, suggest_series_id_optimization
from optimeering_beta.models.predictions_data_list import PredictionsDataList
from optimeering_beta.models.predictions_series_list import PredictionsSeriesList
from optimeering_beta.models.predictions_version_list import PredictionsVersionList
from optimeering_beta.models.versioned_series import VersionedSeries
from optimeering_beta.silent_type_cast import silent_type_cast
from pydantic import Field, StrictBool, StrictFloat, StrictInt, StrictStr, validate_call
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
    @log_function_timing
    @suggest_series_id_optimization
    def list_parameters(
        self,
        param: Optional[StrictStr],
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]],
        ] = None,
    ) -> object:
        """Parameter Route

        Allowed values for each parameter used in filters on the **predictions** routes

        :param param: (required)
        :type param: str
        :return: Returns the result object.
        :rtype: object

        :Example:

                >>> from optimeering_beta import Configuration, OptimeeringClient
                >>> configuration = Configuration(host="https://beta.optimeering.com")
                >>> client = OptimeeringClient(configuration=configuration)
                >>> # Post data point - replace ... with correct dataformat documented above
                >>> response = client.predictions_api.list_parameters(...)

        """  # noqa: E501

        _param = self._list_parameters_serialize(
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
        return response

    def _list_parameters_serialize(
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
            _path_params["param"] = param
        # process the query parameters
        # process the header parameters
        # process the form parameters
        # process the body parameter

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/api/predictions/parameters/{param}",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            collection_formats=_collection_formats,
        )

    @validate_call
    @log_function_timing
    @suggest_series_id_optimization
    def list_series(
        self,
        id: Annotated[
            Optional[List[StrictInt]],
            Field(description="ID of the series to retrieve. If not specified, will return all series."),
        ] = None,
        product: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="The product for which series should be retrieved. If not specified, will return series for all products."
            ),
        ] = None,
        unit_type: Annotated[
            Optional[List[StrictStr]],
            Field(description="Unit type. If not specified, will return series for all unit types."),
        ] = None,
        statistic: Annotated[
            Optional[List[StrictStr]],
            Field(description="Statistic type. If not specified, will return series for all statistic types."),
        ] = None,
        area: Annotated[
            Optional[List[StrictStr]],
            Field(description="The name of the area. If not specified, will return all areas."),
        ] = None,
        resolution: Annotated[
            Optional[List[StrictStr]],
            Field(description="Resolution of the series. If not specified, will return series for all resolutions."),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]],
        ] = None,
    ) -> PredictionsSeriesList:
        """List Series


        Returns prediction series.

        To list versions of a series, use the :any:`list_version` method.


        :param id: ID of the series to retrieve. If not specified, will return all series.
        :type id: List[StrictInt]
        :param product: The product for which series should be retrieved. If not specified, will return series for all products.
        :type product: List[StrictStr]
        :param unit_type: Unit type. If not specified, will return series for all unit types.
        :type unit_type: List[StrictStr]
        :param statistic: Statistic type. If not specified, will return series for all statistic types.
        :type statistic: List[StrictStr]
        :param area: The name of the area. If not specified, will return all areas.
        :type area: List[StrictStr]
        :param resolution: Resolution of the series. If not specified, will return series for all resolutions.
        :type resolution: List[StrictStr]
        :return: Returns the result object.
        :rtype: PredictionsSeriesList

        :Example:

                >>> from optimeering_beta import Configuration, OptimeeringClient
                >>> configuration = Configuration(host="https://beta.optimeering.com")
                >>> client = OptimeeringClient(configuration=configuration)
                >>> # Get filtered data point - replace ... with appropriate filters documented above
                >>> response = client.predictions_api.list_series(...)

        """  # noqa: E501

        _param = self._list_series_serialize(
            id=id,
            product=product,
            unit_type=unit_type,
            statistic=statistic,
            area=area,
            resolution=resolution,
            limit=None,
            offset=None,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "PredictionsSeriesList",
            "422": "HTTPValidationError",
        }

        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        response_data.read()
        paginated_response = self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data
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
            next_pagination = self.api_client.call_api(
                method=_param[0],
                url=next_page,
                header_params=_param[2],
                body=_param[3],
                post_params=_param[4],
                _request_timeout=_request_timeout,
            )
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

    def _list_series_serialize(
        self,
        id,
        product,
        unit_type,
        statistic,
        area,
        resolution,
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
        if id is not None:
            id = ",".join(str(i) for i in id)
            _query_params.append(("id", id))

        if product is not None:
            product = ",".join(str(i) for i in product)
            _query_params.append(("product", product))

        if unit_type is not None:
            unit_type = ",".join(str(i) for i in unit_type)
            _query_params.append(("unit_type", unit_type))

        if statistic is not None:
            statistic = ",".join(str(i) for i in statistic)
            _query_params.append(("statistic", statistic))

        if area is not None:
            area = ",".join(str(i) for i in area)
            _query_params.append(("area", area))

        if resolution is not None:
            resolution = ",".join(str(i) for i in resolution)
            _query_params.append(("resolution", resolution))

        if limit is not None:
            _query_params.append(("limit", limit))

        if offset is not None:
            _query_params.append(("offset", offset))

        # process the header parameters
        # process the form parameters
        # process the body parameter

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
    @log_function_timing
    @suggest_series_id_optimization
    def list_version(
        self,
        id: Annotated[
            Optional[List[StrictInt]],
            Field(description="ID of the series to retrieve. If not specified, will return all series."),
        ] = None,
        product: Annotated[
            Optional[List[StrictStr]],
            Field(
                description="The product for which series should be retrieved. If not specified, will return series for all products."
            ),
        ] = None,
        unit_type: Annotated[
            Optional[List[StrictStr]],
            Field(description="Unit type. If not specified, will return series for all unit types."),
        ] = None,
        statistic: Annotated[
            Optional[List[StrictStr]],
            Field(description="Statistic type. If not specified, will return series for all statistic types."),
        ] = None,
        area: Annotated[
            Optional[List[StrictStr]],
            Field(description="The name of the area. If not specified, will return all areas."),
        ] = None,
        resolution: Annotated[
            Optional[List[StrictStr]],
            Field(description="Resolution of the series. If not specified, will return series for all resolutions."),
        ] = None,
        limit: Annotated[
            Optional[Annotated[int, Field(le=100000, strict=True, ge=1)]], Field(description="Number of items per page")
        ] = None,
        offset: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="Page offset")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]],
        ] = None,
    ) -> PredictionsVersionList:
        """List Series Version


        Returns prediction series and their versions.



        :param id: ID of the series to retrieve. If not specified, will return all series.
        :type id: str
        :param product: The product for which series should be retrieved. If not specified, will return series for all products.
        :type product: str
        :param unit_type: Unit type. If not specified, will return series for all unit types.
        :type unit_type: str
        :param statistic: Statistic type. If not specified, will return series for all statistic types.
        :type statistic: str
        :param area: The name of the area. If not specified, will return all areas.
        :type area: str
        :param resolution: Resolution of the series. If not specified, will return series for all resolutions.
        :type resolution: str
        :param limit: Number of items per page
        :type limit: int
        :param offset: Page offset
        :type offset: int
        :return: Returns the result object.
        :rtype: PredictionsVersionList

        :Example:

                >>> from optimeering_beta import Configuration, OptimeeringClient
                >>> configuration = Configuration(host="https://beta.optimeering.com")
                >>> client = OptimeeringClient(configuration=configuration)
                >>> # Post data point - replace ... with correct dataformat documented above
                >>> response = client.predictions_api.list_version(...)

        """  # noqa: E501

        _param = self._list_version_serialize(
            id=id,
            product=product,
            unit_type=unit_type,
            statistic=statistic,
            area=area,
            resolution=resolution,
            limit=limit,
            offset=offset,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "PredictionsVersionList",
            "422": "HTTPValidationError",
        }

        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        response_data.read()
        response = self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data
        return response

    def _list_version_serialize(
        self,
        id,
        product,
        unit_type,
        statistic,
        area,
        resolution,
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
        if id is not None:
            id = ",".join(str(i) for i in id)
            _query_params.append(("id", id))

        if product is not None:
            product = ",".join(str(i) for i in product)
            _query_params.append(("product", product))

        if unit_type is not None:
            unit_type = ",".join(str(i) for i in unit_type)
            _query_params.append(("unit_type", unit_type))

        if statistic is not None:
            statistic = ",".join(str(i) for i in statistic)
            _query_params.append(("statistic", statistic))

        if area is not None:
            area = ",".join(str(i) for i in area)
            _query_params.append(("area", area))

        if resolution is not None:
            resolution = ",".join(str(i) for i in resolution)
            _query_params.append(("resolution", resolution))

        if limit is not None:
            _query_params.append(("limit", limit))

        if offset is not None:
            _query_params.append(("offset", offset))

        # process the header parameters
        # process the form parameters
        # process the body parameter

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/api/predictions/series_version/",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            collection_formats=_collection_formats,
        )

    @validate_call
    @log_function_timing
    @suggest_series_id_optimization
    def retrieve(
        self,
        series_id: Annotated[
            Optional[List[StrictInt]],
            Field(description="Series ID to filter. If not specified, will return all series."),
        ] = None,
        start: Annotated[
            Optional[Any],
            Field(
                description="The first datetime to fetch (inclusive). Defaults to `1970-01-01 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)"
            ),
        ] = None,
        end: Annotated[
            Optional[Any],
            Field(
                description="The last datetime to fetch (exclusive). Defaults to `2999-12-30 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)"
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]],
        ] = None,
    ) -> PredictionsDataList:
        """Retrieve


        Returns predictions.

        If multiple versions of a prediction exist for a given series, the highest version is returned.

        To get predictions for a particular version, use the :any:`retrieve_versioned` method.


        :param series_id: Series ID to filter. If not specified, will return all series.
        :type series_id: List[StrictInt]
        :param start: The first datetime to fetch (inclusive). Defaults to `1970-01-01 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        :type start: Start
        :param end: The last datetime to fetch (exclusive). Defaults to `2999-12-30 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        :type end: End
        :return: Returns the result object.
        :rtype: PredictionsDataList

        :Example:

                >>> from optimeering_beta import Configuration, OptimeeringClient
                >>> configuration = Configuration(host="https://beta.optimeering.com")
                >>> client = OptimeeringClient(configuration=configuration)
                >>> # Get filtered data point - replace ... with appropriate filters documented above
                >>> response = client.predictions_api.retrieve(...)

        """  # noqa: E501

        _param = self._retrieve_serialize(
            series_id=series_id,
            start=start,
            end=end,
            limit=None,
            offset=None,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "PredictionsDataList",
            "422": "HTTPValidationError",
        }

        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        response_data.read()
        paginated_response = self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data
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
            next_pagination = self.api_client.call_api(
                method=_param[0],
                url=next_page,
                header_params=_param[2],
                body=_param[3],
                post_params=_param[4],
                _request_timeout=_request_timeout,
            )
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

    def _retrieve_serialize(
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

    @validate_call
    @log_function_timing
    @suggest_series_id_optimization
    def retrieve_latest(
        self,
        max_event_time: Annotated[
            Optional[Any],
            Field(
                description="If specified, will only return the latest prediction available at the specified time. If not specified, no filters are applied. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)"
            ),
        ] = None,
        series_id: Annotated[
            Optional[List[StrictInt]],
            Field(description="Series ID to filter. If not specified, will return all series."),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]],
        ] = None,
    ) -> PredictionsDataList:
        """Retrieve Latest


        Returns predictions with the most recent ``event_time``.

        If multiple versions of a prediction exist for a given series, the highest version is returned.

        To get predictions for a particular version, use the :any:`retrieve_versioned`  method.


        :param max_event_time: If specified, will only return the latest prediction available at the specified time. If not specified, no filters are applied. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        :type max_event_time: MaxEventTime
        :param series_id: Series ID to filter. If not specified, will return all series.
        :type series_id: List[StrictInt]
        :return: Returns the result object.
        :rtype: PredictionsDataList

        :Example:

                >>> from optimeering_beta import Configuration, OptimeeringClient
                >>> configuration = Configuration(host="https://beta.optimeering.com")
                >>> client = OptimeeringClient(configuration=configuration)
                >>> # Get filtered data point - replace ... with appropriate filters documented above
                >>> response = client.predictions_api.retrieve_latest(...)

        """  # noqa: E501

        _param = self._retrieve_latest_serialize(
            max_event_time=max_event_time,
            series_id=series_id,
            limit=None,
            offset=None,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "PredictionsDataList",
            "422": "HTTPValidationError",
        }

        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        response_data.read()
        paginated_response = self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data
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
            next_pagination = self.api_client.call_api(
                method=_param[0],
                url=next_page,
                header_params=_param[2],
                body=_param[3],
                post_params=_param[4],
                _request_timeout=_request_timeout,
            )
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

    def _retrieve_latest_serialize(
        self,
        max_event_time,
        series_id,
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
        if max_event_time is not None:
            _query_params.append(("max_event_time", max_event_time))

        if series_id is not None:
            series_id = ",".join(str(i) for i in series_id)
            _query_params.append(("series_id", series_id))

        if limit is not None:
            _query_params.append(("limit", limit))

        if offset is not None:
            _query_params.append(("offset", offset))

        # process the header parameters
        # process the form parameters
        # process the body parameter

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/api/predictions/latest",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            collection_formats=_collection_formats,
        )

    @validate_call
    @log_function_timing
    @silent_type_cast
    @suggest_series_id_optimization
    def retrieve_versioned(
        self,
        versioned_series: Annotated[List[VersionedSeries] | PredictionsVersionList, Field(min_length=1)],
        include_simulated: Annotated[
            Optional[StrictBool], Field(description="If false, filters out simulated prediction from response.")
        ] = None,
        start: Annotated[
            Optional[Any],
            Field(
                description="The first datetime to fetch (inclusive). Defaults to `1970-01-01 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)"
            ),
        ] = None,
        end: Annotated[
            Optional[Any],
            Field(
                description="The last datetime to fetch (exclusive). Defaults to `2999-12-30 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)"
            ),
        ] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]],
        ] = None,
    ) -> PredictionsDataList:
        """Retrive Versioned


        Returns versioned predictions.


        Use the :any:`list_version` method to get the available versions for each prediction series.

        Can be used to retrieve both versioned and simulated data. For an explanation on versioned and simulated data see `Prediction Versioning <https://docs.optimeering.com/getting-started/prediction-versioning/>`_


        :param versioned_series: (required)
        :type versioned_series: List[VersionedSeries] | PredictionsVersionList
        :param include_simulated: If false, filters out simulated prediction from response.
        :type include_simulated: bool
        :param start: The first datetime to fetch (inclusive). Defaults to `1970-01-01 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        :type start: Start
        :param end: The last datetime to fetch (exclusive). Defaults to `2999-12-30 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        :type end: End
        :return: Returns the result object.
        :rtype: PredictionsDataList

        :Example:

                >>> from optimeering_beta import Configuration, OptimeeringClient
                >>> configuration = Configuration(host="https://beta.optimeering.com")
                >>> client = OptimeeringClient(configuration=configuration)
                >>> # Get filtered data point - replace ... with appropriate filters documented above
                >>> response = client.predictions_api.retrieve_versioned(...)

        """  # noqa: E501

        _param = self._retrieve_versioned_serialize(
            versioned_series=versioned_series,
            include_simulated=include_simulated,
            start=start,
            end=end,
            limit=None,
            offset=None,
        )

        _response_types_map: Dict[str, Optional[str]] = {
            "200": "PredictionsDataList",
            "422": "HTTPValidationError",
        }

        response_data = self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        response_data.read()
        paginated_response = self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data
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
            next_pagination = self.api_client.call_api(
                method=_param[0],
                url=next_page,
                header_params=_param[2],
                body=_param[3],
                post_params=_param[4],
                _request_timeout=_request_timeout,
            )
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

    def _retrieve_versioned_serialize(
        self,
        versioned_series,
        include_simulated,
        start,
        end,
        limit,
        offset,
    ) -> RequestSerialized:
        _collection_formats: Dict[str, str] = {
            "VersionedSeries": "",
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, Union[str, bytes]] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        if include_simulated is not None:
            _query_params.append(("include_simulated", include_simulated))

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
        if versioned_series is not None:
            _body_params = versioned_series

        return self.api_client.param_serialize(
            method="POST",
            resource_path="/api/predictions/versioned",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            collection_formats=_collection_formats,
        )
