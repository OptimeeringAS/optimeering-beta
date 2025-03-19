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
from warnings import warn

import optimeering_beta
import orjson
from optimeering_beta.extras import pd, pydantic_to_pandas, require_pandas
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, model_validator


class PredictionsSeries(BaseModel):
    """
    A :any:`PredictionsSeries` is used for indexing a series of :any:`PredictionsData`.

    :param area: Areas to be filtered. E.g. NO1, NO2
    :type area: str
    :param created_at:
    :type created_at: datetime
    :param description:
    :type description: str
    :param id:
    :type id: int
    :param latest_event_time:
    :type latest_event_time: datetime
    :param product: Product name for the series
    :type product: str
    :param resolution: Resolution of the series.
    :type resolution: str
    :param statistic: Type of statistics.
    :type statistic: str
    :param unit: The unit for the series.
    :type unit: str
    :param unit_type: Unit type for the series
    :type unit_type: str
    """  # noqa: E501

    area: StrictStr = Field(description="Areas to be filtered. E.g. NO1, NO2")
    created_at: datetime
    description: Optional[StrictStr] = None
    id: StrictInt
    latest_event_time: Optional[datetime] = None
    product: StrictStr = Field(description="Product name for the series")
    resolution: StrictStr = Field(description="Resolution of the series.")
    statistic: StrictStr = Field(description="Type of statistics.")
    unit: StrictStr = Field(description="The unit for the series.")
    unit_type: StrictStr = Field(description="Unit type for the series")
    _client: Any = None

    __properties: ClassVar[List[str]] = [
        "area",
        "created_at",
        "description",
        "id",
        "latest_event_time",
        "product",
        "resolution",
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
        return orjson.dumps(self.to_dict()).decode()

    @classmethod
    def from_json(cls, json_str: str) -> Optional[PredictionsSeries]:
        """Create an instance of PredictionsSeries from a JSON string"""
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
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[PredictionsSeries]:
        """Create an instance of PredictionsSeries from a dict"""
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
                "resolution": obj.get("resolution"),
                "statistic": obj.get("statistic"),
                "unit": obj.get("unit"),
                "unit_type": obj.get("unit_type"),
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

    def datapoints(
        self,
        start: Optional[datetime | StrictStr] = None,
        end: Optional[datetime | StrictStr] = None,
    ) -> optimeering_beta.models.PredictionsDataList:
        """

        Returns predictions.

        If multiple versions of a prediction exist for a given series, the highest version is returned.

        To get predictions for a particular version, use the :any:`retrieve_versioned` method.


                :param start: The first datetime to fetch (inclusive). Defaults to `1970-01-01 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
                :param end: The last datetime to fetch (exclusive). Defaults to `2999-12-30 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        """
        warn("This method will be deprecated. Use `retrieve` instead.")
        if self._client is None:
            raise AttributeError("Cannot call datapoints method on this instance. The client has not been setup.")

        return optimeering_beta.PredictionsApi(api_client=self._client).retrieve(
            series_id=[self.id],
            start=start,
            end=end,
        )

    def retrieve(
        self,
        start: Optional[datetime | StrictStr] = None,
        end: Optional[datetime | StrictStr] = None,
    ) -> optimeering_beta.models.PredictionsDataList:
        """

        Returns predictions.

        If multiple versions of a prediction exist for a given series, the highest version is returned.

        To get predictions for a particular version, use the :any:`retrieve_versioned` method.


                :param start: The first datetime to fetch (inclusive). Defaults to `1970-01-01 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
                :param end: The last datetime to fetch (exclusive). Defaults to `2999-12-30 00:00:00+0000`. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        """
        if self._client is None:
            raise AttributeError("Cannot call datapoints method on this instance. The client has not been setup.")

        return optimeering_beta.PredictionsApi(api_client=self._client).retrieve(
            series_id=[self.id],
            start=start,
            end=end,
        )

    def retrieve_latest(
        self,
        max_event_time: Optional[datetime | StrictStr] = None,
    ) -> optimeering_beta.models.PredictionsDataList:
        """

        Returns predictions with the most recent ``event_time``.

        If multiple versions of a prediction exist for a given series, the highest version is returned.

        To get predictions for a particular version, use the :any:`retrieve_versioned`  method.


                :param max_event_time: If specified, will only return the latest prediction available at the specified time. If not specified, no filters are applied. Should be specified in ISO 8601 datetime or duration format (eg - `2024-05-15T06:00:00+00:00`, `PT1H`, `-P1W1D`)
        """
        if self._client is None:
            raise AttributeError("Cannot call datapoints method on this instance. The client has not been setup.")

        return optimeering_beta.PredictionsApi(api_client=self._client).retrieve_latest(
            series_id=[self.id],
            max_event_time=max_event_time,
        )

    def list_version(
        self,
        product: Optional[List[StrictStr]] = None,
        unit_type: Optional[List[StrictStr]] = None,
        statistic: Optional[List[StrictStr]] = None,
        area: Optional[List[StrictStr]] = None,
        resolution: Optional[List[StrictStr]] = None,
    ) -> optimeering_beta.models.PredictionsVersionList:
        """

        Returns prediction series and their versions.



                :param product: The product for which series should be retrieved. If not specified, will return series for all products.
                :param unit_type: Unit type. If not specified, will return series for all unit types.
                :param statistic: Statistic type. If not specified, will return series for all statistic types.
                :param area: The name of the area. If not specified, will return all areas.
                :param resolution: Resolution of the series. If not specified, will return series for all resolutions.
        """
        if self._client is None:
            raise AttributeError("Cannot call datapoints method on this instance. The client has not been setup.")

        return optimeering_beta.PredictionsApi(api_client=self._client).list_version(
            id=[self.id],
            product=product,
            unit_type=unit_type,
            statistic=statistic,
            area=area,
            resolution=resolution,
        )

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
