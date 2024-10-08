# coding: utf-8

"""
    Optimeering

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing_extensions import Self


class PredictionsCreatedSeries(BaseModel):
    """
    PredictionsCreatedSeries
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
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of PredictionsCreatedSeries from a JSON string"""
        return cls.from_dict(json.loads(json_str))

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
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PredictionsCreatedSeries from a dict"""
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
