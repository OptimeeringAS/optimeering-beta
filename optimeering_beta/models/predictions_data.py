# coding: utf-8

"""
    Optimeering

"""  # noqa: E501

from __future__ import annotations

import pprint
import re  # noqa: F401
from typing import Any, ClassVar, Dict, List, Optional, Set

import orjson
from optimeering_beta.extras import pd, pydantic_to_pandas, require_pandas
from optimeering_beta.models.predictions_event import PredictionsEvent
from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator
from typing_extensions import Annotated


class PredictionsData(BaseModel):
    """
    :any:`PredictionsData` contains a collection of :any:`PredictionsEvent` for a given :any:`PredictionSeries`

    :param events:
    :type events: List[PredictionsEvent]
    :param series_id: Identifier for the series id.
    :type series_id: int
    :param version: Version of the model that generated the predictions
    :type version: str
    """  # noqa: E501

    events: List[PredictionsEvent]
    series_id: StrictInt = Field(description="Identifier for the series id.")
    version: Annotated[str, Field(strict=True)] = Field(
        description="Version of the model that generated the predictions"
    )
    __properties: ClassVar[List[str]] = ["events", "series_id", "version"]

    @field_validator("version")
    def version_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"[0-9]+\.[0-9]+\.[0-9]+", value):
            raise ValueError(r"must validate the regular expression /[0-9]+\.[0-9]+\.[0-9]+/")
        return value

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
    def from_json(cls, json_str: str) -> Optional[PredictionsData]:
        """Create an instance of PredictionsData from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in events (list)
        _items = []
        if self.events:
            for _item_events in self.events:
                if _item_events:
                    _items.append(_item_events.to_dict())
            _dict["events"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[PredictionsData]:
        """Create an instance of PredictionsData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "events": [PredictionsEvent.from_dict(_item) for _item in obj["events"]]
                if obj.get("events") is not None
                else None,
                "series_id": obj.get("series_id"),
                "version": obj.get("version"),
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
