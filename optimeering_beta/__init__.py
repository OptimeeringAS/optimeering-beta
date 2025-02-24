# coding: utf-8

# flake8: noqa

"""
    Optimeering

"""  # noqa: E501

__version__ = "0.0.7"

# import apis into sdk package
from optimeering_beta.api.access_api import AccessApi
from optimeering_beta.api.predictions_api import PredictionsApi
from optimeering_beta.api_client import OptimeeringClient

# import OptimeeringClient
from optimeering_beta.api_response import ApiResponse
from optimeering_beta.azure_authentication import AzureAuth
from optimeering_beta.configuration import Configuration
from optimeering_beta.exceptions import (
    ApiAttributeError,
    ApiException,
    ApiKeyError,
    ApiTypeError,
    ApiValueError,
    OpenApiException,
)

# import models into sdk package
from optimeering_beta.models.access_key_created import AccessKeyCreated
from optimeering_beta.models.access_key_post_response import AccessKeyPostResponse
from optimeering_beta.models.access_post_key import AccessPostKey
from optimeering_beta.models.end import End
from optimeering_beta.models.http_validation_error import HTTPValidationError
from optimeering_beta.models.max_event_time import MaxEventTime
from optimeering_beta.models.predictions_data import PredictionsData
from optimeering_beta.models.predictions_data_list import PredictionsDataList
from optimeering_beta.models.predictions_event import PredictionsEvent
from optimeering_beta.models.predictions_series import PredictionsSeries
from optimeering_beta.models.predictions_series_list import PredictionsSeriesList
from optimeering_beta.models.predictions_value import PredictionsValue
from optimeering_beta.models.predictions_version import PredictionsVersion
from optimeering_beta.models.predictions_version_list import PredictionsVersionList
from optimeering_beta.models.start import Start
from optimeering_beta.models.validation_error import ValidationError
from optimeering_beta.models.validation_error_loc_inner import ValidationErrorLocInner
from optimeering_beta.models.versioned_series import VersionedSeries

# add to __all__
__all__ = [
    "AccessApi",
    "PredictionsApi",
    "ApiResponse",
    "AzureAuth",
    "OptimeeringClient",
    "Configuration",
    "OpenApiException",
    "ApiTypeError",
    "ApiValueError",
    "ApiKeyError",
    "ApiAttributeError",
    "ApiException",
    "AccessKeyCreated",
    "AccessKeyPostResponse",
    "AccessPostKey",
    "End",
    "HTTPValidationError",
    "MaxEventTime",
    "PredictionsData",
    "PredictionsDataList",
    "PredictionsEvent",
    "PredictionsSeries",
    "PredictionsSeriesList",
    "PredictionsValue",
    "PredictionsVersion",
    "PredictionsVersionList",
    "Start",
    "ValidationError",
    "ValidationErrorLocInner",
    "VersionedSeries",
]
