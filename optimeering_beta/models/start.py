# coding: utf-8

"""
    Optimeering

"""  # noqa: E501

from __future__ import annotations

import pprint
import re  # noqa: F401
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Set, Union

import orjson
from pydantic import BaseModel, ValidationError, field_validator

START_ANY_OF_SCHEMAS = ["datetime", "str"]


class Start(BaseModel):
    """
    The first datetime to fetch (inclusive). Defaults to `1970-01-01 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
    """

    # data type: str
    anyof_schema_1_validator: Optional[timedelta] = None

    # data type: datetime
    anyof_schema_2_validator: Optional[datetime] = None
    actual_instance: Any = None
    any_of_schemas: Set[str] = {"datetime", "str"}

    model_config = {
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(actual_instance=kwargs)

    @field_validator("actual_instance")
    def actual_instance_must_validate_anyof(cls, v):
        if v is None:
            return v

        instance = Start.model_construct()  # noqa: F841
        error_messages = []
        # validate data type: str
        try:
            instance.anyof_schema_1_validator = v
            return v
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: datetime
        try:
            instance.anyof_schema_2_validator = v
            return v
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        if error_messages:
            # no match
            raise ValueError(
                "No match found when setting the actual_instance in Start with anyOf schemas: datetime, str. Details: "
                + ", ".join(error_messages)
            )
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Start:
        return cls.from_json(orjson.dumps(obj).decode())

    @classmethod
    def from_json(cls, json_str: str) -> Start:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        if json_str is None:
            return instance

        error_messages = []
        # deserialize data into str
        try:
            # validation
            instance.anyof_schema_1_validator = orjson.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.anyof_schema_1_validator
            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into datetime
        try:
            # validation
            instance.anyof_schema_2_validator = orjson.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.anyof_schema_2_validator
            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if error_messages:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into Start with anyOf schemas: datetime, str. Details: "
                + ", ".join(error_messages)
            )
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return orjson.dumps(self.actual_instance).decode()

    def to_dict(self) -> Optional[Union[Dict[str, Any], datetime, str]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())
