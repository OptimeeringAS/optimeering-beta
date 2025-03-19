# coding: utf-8

"""
    Optimeering

"""  # noqa: E501

from __future__ import annotations

import pprint
import re  # noqa: F401
import warnings
from typing import Any, ClassVar, Dict, List, Optional, Set

import orjson
from optimeering_beta.extras import pd, pydantic_to_pandas, require_pandas
from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator, model_validator
from typing_extensions import Annotated


class VersionedSeries(BaseModel):
    """
    A :any:`VersionedSeries` can be used with :any:`retrieve_versioned` to specify a version of a series to retrieve.

    :param series_id: Id of the series
    :type series_id: int
    :param version: Version number of the series to filter
    :type version: str
    """  # noqa: E501

    series_id: StrictInt = Field(description="Id of the series")
    version: Annotated[str, Field(strict=True)] = Field(description="Version number of the series to filter")

    __properties: ClassVar[List[str]] = ["series_id", "version"]

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
    def from_json(cls, json_str: str) -> Optional[VersionedSeries]:
        """Create an instance of VersionedSeries from a JSON string"""
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
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[VersionedSeries]:
        """Create an instance of VersionedSeries from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({"series_id": obj.get("series_id"), "version": obj.get("version")})
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
