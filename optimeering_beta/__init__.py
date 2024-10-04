# coding: utf-8

# flake8: noqa

"""
    Optimeering

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


__version__ = "0.0.4"

# import apis into sdk package
from optimeering_beta.api.access_api import AccessApi
from optimeering_beta.api.parameters_api import ParametersApi
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
from optimeering_beta.models.enum_parameters import EnumParameters
from optimeering_beta.models.http_validation_error import HTTPValidationError
from optimeering_beta.models.location_inner import LocationInner
from optimeering_beta.models.max_event_time import MaxEventTime
from optimeering_beta.models.prediction_float_model import PredictionFloatModel
from optimeering_beta.models.predictions_created_series import PredictionsCreatedSeries
from optimeering_beta.models.predictions_data_get_response import PredictionsDataGetResponse
from optimeering_beta.models.predictions_dict_model import PredictionsDictModel
from optimeering_beta.models.predictions_inner import PredictionsInner
from optimeering_beta.models.predictions_series_get_response import PredictionsSeriesGetResponse
from optimeering_beta.models.predictions_single_event_data_created import PredictionsSingleEventDataCreated
from optimeering_beta.models.predictions_single_series_data_created import PredictionsSingleSeriesDataCreated
from optimeering_beta.models.start import Start
from optimeering_beta.models.validation_error import ValidationError

# add to __all__
__all__ = [
    "AccessApi",
    "ParametersApi",
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
    "EnumParameters",
    "HTTPValidationError",
    "LocationInner",
    "MaxEventTime",
    "PredictionFloatModel",
    "PredictionsCreatedSeries",
    "PredictionsDataGetResponse",
    "PredictionsDictModel",
    "PredictionsInner",
    "PredictionsSeriesGetResponse",
    "PredictionsSingleEventDataCreated",
    "PredictionsSingleSeriesDataCreated",
    "Start",
    "ValidationError",
]
