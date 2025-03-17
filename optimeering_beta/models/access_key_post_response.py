# coding: utf-8

"""
    Optimeering

"""  # noqa: E501

from __future__ import annotations

import pprint
import re  # noqa: F401
import warnings
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Set

import orjson
from optimeering_beta.extras import pd, pydantic_to_pandas, require_pandas
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, model_validator


class AccessKeyPostResponse(BaseModel):
    """
    AccessKeyPostResponse

    :param apikey: API key
    :type apikey: str
    :param created_at: Time stamp at which key was created.
    :type created_at: datetime
    :param description: Description for the Access key.
    :type description: str
    :param expires_at: Duration after which key expires.
    :type expires_at: datetime
    :param id: ID of the access key
    :type id: int
    :param owner_id: Creator of the access key.
    :type owner_id: str
    """  # noqa: E501

    apikey: StrictStr = Field(description="API key")
    created_at: datetime = Field(description="Time stamp at which key was created.")
    description: StrictStr = Field(description="Description for the Access key.")
    expires_at: datetime = Field(description="Duration after which key expires.")
    id: StrictInt = Field(description="ID of the access key")
    owner_id: StrictStr = Field(description="Creator of the access key.")
    __properties: ClassVar[List[str]] = ["apikey", "created_at", "description", "expires_at", "id", "owner_id"]

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
    def from_json(cls, json_str: str) -> Optional[AccessKeyPostResponse]:
        """Create an instance of AccessKeyPostResponse from a JSON string"""
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
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[AccessKeyPostResponse]:
        """Create an instance of AccessKeyPostResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "apikey": obj.get("apikey"),
                "created_at": obj.get("created_at"),
                "description": obj.get("description"),
                "expires_at": obj.get("expires_at"),
                "id": obj.get("id"),
                "owner_id": obj.get("owner_id"),
            }
        )
        return _obj

    @model_validator(mode="before")
    def validate_extra_fields(cls, values):
        if len(values) > 1:  # Check if there are extra fields
            if set(values) - set(cls.model_fields):
                warnings.warn("Data mismatch, please update the SDK to the latest version")
        return values

    def __len__(self):
        return 1

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
