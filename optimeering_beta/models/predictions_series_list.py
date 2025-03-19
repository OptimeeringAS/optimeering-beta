# coding: utf-8

"""
    Optimeering

"""  # noqa: E501

from __future__ import annotations

import pprint
import re  # noqa: F401
import warnings
from datetime import datetime
from typing import Any, ClassVar, Dict, Iterable, Iterator, List, Optional, Set
from warnings import warn

import optimeering_beta
import orjson
from optimeering_beta.extras import pd, pydantic_to_pandas, require_pandas
from optimeering_beta.models.predictions_series import PredictionsSeries
from pydantic import BaseModel, ConfigDict, Field, StrictStr, model_validator


class PredictionsSeriesList(BaseModel):
    """
    A :any:`PredictionsSeriesList` contains a collection of :any:`PredictionsSeries`.

    :param items:
    :type items: List[PredictionsSeries]
    :param next_page: The next page of results (if available).
    :type next_page: str
    """  # noqa: E501

    items: List[PredictionsSeries]
    next_page: Optional[StrictStr] = Field(default=None, description="The next page of results (if available).")
    _client: Any = None

    __properties: ClassVar[List[str]] = ["items", "next_page"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return orjson.dumps(self.to_dict()).decode()

    @classmethod
    def from_json(cls, json_str: str) -> Optional[PredictionsSeriesList]:
        """Create an instance of PredictionsSeriesList from a JSON string"""
        return cls.from_dict(orjson.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in items (list)
        _items = []
        if self.items:
            for _item_items in self.items:
                if _item_items:
                    _items.append(_item_items.to_dict())
            _dict["items"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[PredictionsSeriesList]:
        """Create an instance of PredictionsSeriesList from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "items": [PredictionsSeries.from_dict(_item) for _item in obj["items"]]
                if obj.get("items") is not None
                else None,
                "next_page": obj.get("next_page"),
            }
        )
        return _obj

    @model_validator(mode="before")
    def validate_extra_fields(cls, values):
        if isinstance(values, Dict):
            values_private_removed = {k: v for k, v in values.items() if not k.startswith("_")}
        else:
            values_private_removed = values
        if len(values_private_removed) > 1:  # Check if there are extra fields
            if set(values_private_removed) - set(cls.model_fields):
                warnings.warn("Data mismatch, please update the SDK to the latest version")
        return values

    @property
    def series_ids(self) -> List[int]:
        """Returns all the series ids included in the response"""
        iterate_over: Iterable
        if "items" in self.model_fields:
            iterate_over = self.items
        else:
            iterate_over = self
        return list({getattr(i, "id") for i in iterate_over})

    def datapoints(
        self,
        start: Optional[datetime | StrictStr] = None,
        end: Optional[datetime | StrictStr] = None,
    ) -> optimeering_beta.models.PredictionsDataList:
        """

        Returns predictions.

        If multiple versions of a prediction exist for a given series, the highest version is returned.

        To get predictions for a particular version, use the :any:`retrieve_versioned` method.


                :param start: The first datetime to fetch (inclusive). Defaults to `1970-01-01 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
                :param end: The last datetime to fetch (exclusive). Defaults to `2999-12-30 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        """
        warn("This method will be deprecated. Use `retrieve` instead.")
        if self._client is None:
            raise AttributeError("Cannot call datapoints method on this instance. The client has not been setup.")

        return optimeering_beta.PredictionsApi(api_client=self._client).retrieve(
            series_id=self.series_ids,
            start=start,
            end=end,
        )

    def retrieve(
        self,
        start: Optional[datetime | StrictStr] = None,
        end: Optional[datetime | StrictStr] = None,
    ) -> optimeering_beta.models.PredictionsDataList:
        """

        Returns predictions.

        If multiple versions of a prediction exist for a given series, the highest version is returned.

        To get predictions for a particular version, use the :any:`retrieve_versioned` method.


                :param start: The first datetime to fetch (inclusive). Defaults to `1970-01-01 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
                :param end: The last datetime to fetch (exclusive). Defaults to `2999-12-30 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        """
        if self._client is None:
            raise AttributeError("Cannot call datapoints method on this instance. The client has not been setup.")

        return optimeering_beta.PredictionsApi(api_client=self._client).retrieve(
            series_id=self.series_ids,
            start=start,
            end=end,
        )

    def retrieve_latest(
        self,
        max_event_time: Optional[datetime | StrictStr] = None,
    ) -> optimeering_beta.models.PredictionsDataList:
        """

        Returns predictions with the most recent ``event_time``.

        If multiple versions of a prediction exist for a given series, the highest version is returned.

        To get predictions for a particular version, use the :any:`retrieve_versioned`  method.


                :param max_event_time: If specified, will only return the latest prediction available at the specified time. If not specified, no filters are applied. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        """
        if self._client is None:
            raise AttributeError("Cannot call datapoints method on this instance. The client has not been setup.")

        return optimeering_beta.PredictionsApi(api_client=self._client).retrieve_latest(
            series_id=self.series_ids,
            max_event_time=max_event_time,
        )

    def list_version(
        self,
        product: Optional[List[StrictStr]] = None,
        unit_type: Optional[List[StrictStr]] = None,
        statistic: Optional[List[StrictStr]] = None,
        area: Optional[List[StrictStr]] = None,
        resolution: Optional[List[StrictStr]] = None,
    ) -> optimeering_beta.models.PredictionsVersionList:
        """

        Returns prediction series and their versions.



                :param product: The product for which series should be retrieved. If not specified, will return series for all products.
                :param unit_type: Unit type. If not specified, will return series for all unit types.
                :param statistic: Statistic type. If not specified, will return series for all statistic types.
                :param area: The name of the area. If not specified, will return all areas.
                :param resolution: Resolution of the series. If not specified, will return series for all resolutions.
        """
        if self._client is None:
            raise AttributeError("Cannot call datapoints method on this instance. The client has not been setup.")

        return optimeering_beta.PredictionsApi(api_client=self._client).list_version(
            id=self.series_ids,
            product=product,
            unit_type=unit_type,
            statistic=statistic,
            area=area,
            resolution=resolution,
        )

    def __len__(self):
        return sum(len(i) for i in self.items)

    def __iter__(self) -> Iterator[PredictionsSeries]:  # type: ignore[override]
        """Iteration method for generated models"""
        self.__iter_index = 0
        return self

    def __next__(self) -> PredictionsSeries:
        if not self.items:
            raise StopIteration
        try:
            _return = self.items[self.__iter_index]
        except IndexError:
            del self.__iter_index
            raise StopIteration
        else:
            self.__iter_index += 1
            return _return

    def filter(
        self,
        area: Optional[List[str]] = None,
        id: Optional[List[int]] = None,
        product: Optional[List[str]] = None,
        resolution: Optional[List[str]] = None,
        statistic: Optional[List[str]] = None,
        unit: Optional[List[str]] = None,
        unit_type: Optional[List[str]] = None,
    ) -> PredictionsSeriesList:
        """Filters items"""
        properties = [
            "area",
            "id",
            "product",
            "resolution",
            "statistic",
            "unit",
            "unit_type",
        ]
        _locals = locals()
        compare_dict = {i: _locals[i] for i in properties if _locals[i] is not None}

        obj_copy = self.model_copy()
        obj_copy.items = [
            item
            for item in obj_copy
            if all(
                getattr(item, property_name) in filter_values for property_name, filter_values in compare_dict.items()
            )
        ]
        return obj_copy

    @require_pandas
    def to_pandas(
        self,
    ) -> "pd.DataFrame":  # type: ignore[name-defined]
        """
        Converts the object into a pandas dataframe.

        """
        return pydantic_to_pandas(
            self,
        )
