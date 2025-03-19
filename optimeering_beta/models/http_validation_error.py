# coding: utf-8

"""
    Optimeering

"""  # noqa: E501

from __future__ import annotations

import pprint
import re  # noqa: F401
import warnings
from typing import Any, ClassVar, Dict, Iterator, List, Optional, Set

import orjson
from optimeering_beta.extras import pd, pydantic_to_pandas, require_pandas
from optimeering_beta.models.validation_error import ValidationError
from pydantic import BaseModel, ConfigDict, model_validator


class HTTPValidationError(BaseModel):
    """
    HTTPValidationError

    :param detail:
    :type detail: List[ValidationError]
    """  # noqa: E501

    detail: Optional[List[ValidationError]] = None

    __properties: ClassVar[List[str]] = ["detail"]

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
    def from_json(cls, json_str: str) -> Optional[HTTPValidationError]:
        """Create an instance of HTTPValidationError from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in detail (list)
        _items = []
        if self.detail:
            for _item_detail in self.detail:
                if _item_detail:
                    _items.append(_item_detail.to_dict())
            _dict["detail"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[HTTPValidationError]:
        """Create an instance of HTTPValidationError from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "detail": [ValidationError.from_dict(_item) for _item in obj["detail"]]
                if obj.get("detail") is not None
                else None
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

    def __len__(self):
        return sum(len(i) for i in self.detail)

    def __iter__(self) -> Iterator[ValidationError]:  # type: ignore[override]
        """Iteration method for generated models"""
        self.__iter_index = 0
        return self

    def __next__(self) -> ValidationError:
        if not self.detail:
            raise StopIteration
        try:
            _return = self.detail[self.__iter_index]
        except IndexError:
            del self.__iter_index
            raise StopIteration
        else:
            self.__iter_index += 1
            return _return

    def filter(
        self,
        msg: Optional[List[str]] = None,
        type: Optional[List[str]] = None,
    ) -> HTTPValidationError:
        """Filters items"""
        properties = [
            "msg",
            "type",
        ]
        _locals = locals()
        compare_dict = {i: _locals[i] for i in properties if _locals[i] is not None}

        obj_copy = self.model_copy()
        obj_copy.detail = [
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
