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
from optimeering_beta.models.predictions_data import PredictionsData
from pydantic import BaseModel, ConfigDict, Field, StrictStr, model_validator


class PredictionsDataList(BaseModel):
    """
    A :any:`PredictionsDataList` contains a collection of :any:`PredictionsData`

    :param items:
    :type items: List[PredictionsData]
    :param next_page: The next page of results (if available).
    :type next_page: str
    """  # noqa: E501

    items: List[PredictionsData]
    next_page: Optional[StrictStr] = Field(default=None, description="The next page of results (if available).")

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
    def from_json(cls, json_str: str) -> Optional[PredictionsDataList]:
        """Create an instance of PredictionsDataList from a JSON string"""
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
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[PredictionsDataList]:
        """Create an instance of PredictionsDataList from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "items": [PredictionsData.from_dict(_item) for _item in obj["items"]]
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

    def __len__(self):
        return sum(len(i) for i in self.items)

    def __iter__(self) -> Iterator[PredictionsData]:  # type: ignore[override]
        """Iteration method for generated models"""
        self.__iter_index = 0
        return self

    def __next__(self) -> PredictionsData:
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
        series_id: Optional[List[int]] = None,
        version: Optional[List[str]] = None,
    ) -> PredictionsDataList:
        """Filters items"""
        properties = [
            "series_id",
            "version",
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
    def to_pandas(self, unpack_value_method: str) -> "pd.DataFrame":  # type: ignore[name-defined]
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
