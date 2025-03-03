# coding: utf-8

"""
    Optimeering

"""  # noqa: E501

from __future__ import annotations

import inspect
import pprint
import re  # noqa: F401
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Set

import optimeering_beta
import orjson
from optimeering_beta.extras import pd, pydantic_to_pandas, require_pandas
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr


class PredictionsSeries(BaseModel):
    """
    A :any:`PredictionsSeries` is used for indexing a series of :any:`PredictionsData`.

    :param area: Areas to be filtered. E.g. NO1, NO2
    :type area: str
    :param created_at:
    :type created_at: datetime
    :param description:
    :type description: str
    :param id:
    :type id: int
    :param latest_event_time:
    :type latest_event_time: datetime
    :param product: Product name for the series
    :type product: str
    :param statistic: Type of statistics.
    :type statistic: str
    :param unit: The unit for the series.
    :type unit: str
    :param unit_type: Unit type for the series
    :type unit_type: str
    """  # noqa: E501

    area: StrictStr = Field(description="Areas to be filtered. E.g. NO1, NO2")
    created_at: datetime
    description: Optional[StrictStr] = None
    id: StrictInt
    latest_event_time: Optional[datetime] = None
    product: StrictStr = Field(description="Product name for the series")
    statistic: StrictStr = Field(description="Type of statistics.")
    unit: StrictStr = Field(description="The unit for the series.")
    unit_type: StrictStr = Field(description="Unit type for the series")
    _client: Any = None
    __properties: ClassVar[List[str]] = [
        "area",
        "created_at",
        "description",
        "id",
        "latest_event_time",
        "product",
        "statistic",
        "unit",
        "unit_type",
    ]

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
    def from_json(cls, json_str: str) -> Optional[PredictionsSeries]:
        """Create an instance of PredictionsSeries from a JSON string"""
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
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict["description"] = None

        # set to None if latest_event_time (nullable) is None
        # and model_fields_set contains the field
        if self.latest_event_time is None and "latest_event_time" in self.model_fields_set:
            _dict["latest_event_time"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[PredictionsSeries]:
        """Create an instance of PredictionsSeries from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "area": obj.get("area"),
                "created_at": obj.get("created_at"),
                "description": obj.get("description"),
                "id": obj.get("id"),
                "latest_event_time": obj.get("latest_event_time"),
                "product": obj.get("product"),
                "statistic": obj.get("statistic"),
                "unit": obj.get("unit"),
                "unit_type": obj.get("unit_type"),
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
