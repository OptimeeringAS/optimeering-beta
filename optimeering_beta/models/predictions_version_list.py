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
from optimeering_beta.models.predictions_version import PredictionsVersion
from pydantic import BaseModel, ConfigDict, Field, StrictStr


class PredictionsVersionList(BaseModel):
    """
    A :any:`PredictionsVersionList` contains a collection of :any:`PredictionsVersion`.

    :param items:
    :type items: List[PredictionsVersion]
    :param next_page: The next page of results (if available).
    :type next_page: str
    """  # noqa: E501

    items: List[PredictionsVersion]
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
    def from_json(cls, json_str: str) -> Optional[PredictionsVersionList]:
        """Create an instance of PredictionsVersionList from a JSON string"""
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
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[PredictionsVersionList]:
        """Create an instance of PredictionsVersionList from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "items": [PredictionsVersion.from_dict(_item) for _item in obj["items"]]
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
        version: Optional[List[str]] = None,
    ) -> PredictionsVersionList:
        """Filters items"""
        properties = [
            "area",
            "id",
            "product",
            "statistic",
            "unit",
            "unit_type",
            "version",
        ]
        _locals = locals()
        compare_dict = {i: _locals[i] for i in properties if _locals[i] is not None}

        if isinstance(self, list):
            return [
                item
                for item in self
                if all((item.get(property) in filter_values) for property_name, filter_values in compare_dict.items())
            ]
        elif "items" in self.model_fields:
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

    def convert_to_versioned_series(self) -> List:
        """Converts all items"""
        return [i.convert_to_versioned_series() for i in self.items]

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
