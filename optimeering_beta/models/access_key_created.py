# coding: utf-8

"""
    Optimeering

"""  # noqa: E501

from __future__ import annotations

import pprint
import re  # noqa: F401
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Set

import orjson
from optimeering_beta.extras import pd, pydantic_to_pandas, require_pandas
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr


class AccessKeyCreated(BaseModel):
    """
    AccessKeyCreated

    :param created_at: Time stamp at which key was created.
    :type created_at: datetime
    :param description: Description for the Access key.
    :type description: str
    :param expires_at: Duration after which key expires.
    :type expires_at: datetime
    :param id: ID of the access key
    :type id: int
    """  # noqa: E501

    created_at: datetime = Field(description="Time stamp at which key was created.")
    description: StrictStr = Field(description="Description for the Access key.")
    expires_at: datetime = Field(description="Duration after which key expires.")
    id: StrictInt = Field(description="ID of the access key")
    __properties: ClassVar[List[str]] = ["created_at", "description", "expires_at", "id"]

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
    def from_json(cls, json_str: str) -> Optional[AccessKeyCreated]:
        """Create an instance of AccessKeyCreated from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[AccessKeyCreated]:
        """Create an instance of AccessKeyCreated from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "created_at": obj.get("created_at"),
                "description": obj.get("description"),
                "expires_at": obj.get("expires_at"),
                "id": obj.get("id"),
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
