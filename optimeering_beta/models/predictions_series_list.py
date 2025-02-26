# coding: utf-8

"""
    Optimeering

"""  # noqa: E501

from __future__ import annotations

import inspect
import pprint
import re  # noqa: F401
from datetime import datetime
from typing import Any, ClassVar, Dict, Iterable, List, Optional, Set

import optimeering_beta
import orjson
from optimeering_beta.extras import pd, pydantic_to_pandas, require_pandas
from optimeering_beta.models.predictions_series import PredictionsSeries
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr


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

    def __len__(self):
        if "items" in self.model_fields:
            return sum(len(i) for i in self.items)
        elif "datapoints" in self.model_fields:
            return sum(len(i) for i in self.datapoints)
        elif "predictions" in self.model_fields:
            return sum(len(i) for i in self.predictions)
        elif "entities" in self.model_fields:
            return sum(len(i) for i in self.entities)
        elif "capacity_restrictions" in self.model_fields:
            return sum(len(i) for i in self.capacity_restrictions)
        return 1

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
        include_history: Optional[StrictBool] = None,
    ) -> optimeering_beta.models.PredictionsDataList:
        """
        Returns data points for the current series.

        :param start: The first datetime to fetch (inclusive). Defaults to current time. Should be specified in ISO 8601 format (eg - '2024-05-15T06:00:00+00:00'). Also supports delta formats (e.g. H+1,D-1,W-1)
        :param end: The last datetime to fetch (exclusive). Defaults to 2099-12-30. Should be specified in ISO 8601 format (eg - '2024-05-15T08:00:00+00:00'). Also supports delta formats (e.g. H+1,D-1,W-1)
        :param include_history: Include historical data into the response. Defaults to False. This argument has no effect if the underlying API does not support getting history.
        """
        if self._client is None:
            raise AttributeError("Cannot call datapoints method on this instance. The client has not been setup.")
        method_for_operation = optimeering_beta.PredictionsApi(api_client=self._client).retrieve

        extra_params: Dict[str, Any] = {}
        valid_arguments = list(inspect.signature(method_for_operation).parameters.keys())
        if "include_history" in valid_arguments:
            extra_params["include_history"] = include_history

        if hasattr(self, "series_ids"):
            return method_for_operation(series_id=self.series_ids, start=start, end=end, **extra_params)
        elif hasattr(self, "id"):
            return method_for_operation(series_id=[self.id], start=start, end=end, **extra_params)
        else:
            raise NotImplementedError("This class does not support this feature.")

    def __iter__(self):
        """Iteration method for generated models"""
        if isinstance(self, list):
            return (i for i in self)
        elif "items" in self.model_fields:
            return iter(self.items)
        else:
            raise AttributeError("This object does not support iteration.")

    def filter(
        self,
        area: Optional[List[str]] = None,
        id: Optional[List[int]] = None,
        product: Optional[List[str]] = None,
        statistic: Optional[List[str]] = None,
        unit: Optional[List[str]] = None,
        unit_type: Optional[List[str]] = None,
    ) -> PredictionsSeriesList:
        """Filters items"""
        properties = [
            "area",
            "id",
            "product",
            "statistic",
            "unit",
            "unit_type",
        ]
        _locals = locals()
        compare_dict = {i: _locals[i] for i in properties if _locals[i] is not None}

        if "items" in self.model_fields:
            obj_copy = self.copy()
            obj_copy.items = [
                item
                for item in iter(obj_copy.items)
                if all(
                    getattr(item, property_name) in filter_values
                    for property_name, filter_values in compare_dict.items()
                )
            ]
            return obj_copy
        else:
            raise AttributeError("This object does not support iteration.")

    @require_pandas
    def to_pandas(self, unpack_value_method: Optional[str] = None) -> "pd.DataFrame":  # type: ignore[name-defined]
        """
        Converts the object into a pandas dataframe.

        :param unpack_value_method:
            Determines how values are unpacked. Should be one of the following:
                1. retain_original: Do not unpack the values.
                2. new_rows: A new row will be created in the dataframe for each unpacked value. A new column `value_category` will be added which determines the category of the value.
                3. new_columns: A new column will be created in the dataframe for each unpacked value. The columns for unpacked values will be prepended with `value_`.
        :type unpack_value_method: str
        """
        return pydantic_to_pandas(self, unpack_value_method)
