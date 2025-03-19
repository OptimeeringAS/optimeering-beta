# coding: utf-8

"""
    Optimeering

"""  # noqa: E501

from __future__ import annotations

import pprint
import re  # noqa: F401
import warnings
from datetime import datetime
from typing import Any, ClassVar, Dict, Iterator, List, Optional, Set

import optimeering_beta
import orjson
from optimeering_beta.extras import pd, pydantic_to_pandas, require_pandas
from optimeering_beta.models.predictions_version import PredictionsVersion
from pydantic import BaseModel, ConfigDict, Field, StrictStr, model_validator


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
    _client: Any = None

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

    def retrieve_versioned(
        self,
        include_simulated: Optional[bool] = None,
        start: Optional[datetime | StrictStr] = None,
        end: Optional[datetime | StrictStr] = None,
    ) -> optimeering_beta.models.PredictionsDataList:
        """

        Returns versioned predictions.


        Use the :any:`list_version` method to get the available versions for each prediction series.

        Can be used to retrieve both versioned and simulated data. For an explanation on versioned and simulated data see `Prediction Versioning <https://docs.optimeering.com/getting-started/prediction-versioning/>`_


                :param include_simulated: If false, filters out simulated prediction from response.
                :param start: The first datetime to fetch (inclusive). Defaults to `1970-01-01 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
                :param end: The last datetime to fetch (exclusive). Defaults to `2999-12-30 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        """
        if self._client is None:
            raise AttributeError("Cannot call datapoints method on this instance. The client has not been setup.")

        return optimeering_beta.PredictionsApi(api_client=self._client).retrieve_versioned(
            versioned_series=self,
            include_simulated=include_simulated,
            start=start,
            end=end,
        )

    def __len__(self):
        return sum(len(i) for i in self.items)

    def __iter__(self) -> Iterator[PredictionsVersion]:  # type: ignore[override]
        """Iteration method for generated models"""
        self.__iter_index = 0
        return self

    def __next__(self) -> PredictionsVersion:
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
        area: Optional[List[str]] = None,
        id: Optional[List[int]] = None,
        product: Optional[List[str]] = None,
        resolution: Optional[List[str]] = None,
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
            "resolution",
            "statistic",
            "unit",
            "unit_type",
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

    def convert_to_versioned_series(self) -> List:
        """Converts all items"""
        return [i.convert_to_versioned_series() for i in self.items]

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
