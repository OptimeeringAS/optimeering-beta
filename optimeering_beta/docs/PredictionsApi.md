# optimeering_beta.PredictionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_prediction_series**](PredictionsApi.md#get_prediction_series) | **GET** /api/predictions/series/ | Get Series
[**get_predictions**](PredictionsApi.md#get_predictions) | **GET** /api/predictions/ | Get Predictions


# **get_prediction_series**
> PredsSeriesGetResponse get_prediction_series(name=name, area=area, market=market, statistic=statistic, id=id, unit_type=unit_type, limit=limit, offset=offset)

Get Series

Returns the prediction series

### Example


```python
import optimeering_beta
from optimeering_beta.models.preds_series_get_response import PredsSeriesGetResponse
from optimeering_beta.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = optimeering_beta.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with optimeering_beta.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = optimeering_beta.PredictionsApi(api_client)
    name = 'name_example' # str | Name of the series to retrieve. If not specified, will return all series. (optional)
    area = 'area_example' # str | The name of the area (eg - NO3, SE4, or FI). If not specified, will return all areas. (optional)
    market = 'market_example' # str | The market for which series should be retrieved. If not specified, will return series for all markets. (optional)
    statistic = 'statistic_example' # str | Statistic type (eg. 'size', 'direction', or 'quantile'). If not specified, will return series for all statistic types. (optional)
    id = 'id_example' # str | ID of the series to retrieve. If not specified, will return all series. (optional)
    unit_type = 'unit_type_example' # str | Unit type (eq. 'volumes', 'price', or 'price_spread'). If not specified, will return series for all unit types. (optional)
    limit = 2 # int | Number of items per page (optional)
    offset = 56 # int | Page offset (optional)

    try:
        # Get Series
        api_response = api_instance.get_prediction_series(name=name, area=area, market=market, statistic=statistic, id=id, unit_type=unit_type, limit=limit, offset=offset)
        print("The response of PredictionsApi->get_prediction_series:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PredictionsApi->get_prediction_series: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Name of the series to retrieve. If not specified, will return all series. | [optional] 
 **area** | **str**| The name of the area (eg - NO3, SE4, or FI). If not specified, will return all areas. | [optional] 
 **market** | **str**| The market for which series should be retrieved. If not specified, will return series for all markets. | [optional] 
 **statistic** | **str**| Statistic type (eg. &#39;size&#39;, &#39;direction&#39;, or &#39;quantile&#39;). If not specified, will return series for all statistic types. | [optional] 
 **id** | **str**| ID of the series to retrieve. If not specified, will return all series. | [optional] 
 **unit_type** | **str**| Unit type (eq. &#39;volumes&#39;, &#39;price&#39;, or &#39;price_spread&#39;). If not specified, will return series for all unit types. | [optional] 
 **limit** | **int**| Number of items per page | [optional] 
 **offset** | **int**| Page offset | [optional] 

### Return type

[**PredsSeriesGetResponse**](PredsSeriesGetResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_predictions**
> PredsDataGetResponse get_predictions(series_id=series_id, start=start, end=end, limit=limit, offset=offset)

Get Predictions

Returns predictions

### Example


```python
import optimeering_beta
from optimeering_beta.models.preds_data_get_response import PredsDataGetResponse
from optimeering_beta.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = optimeering_beta.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with optimeering_beta.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = optimeering_beta.PredictionsApi(api_client)
    series_id = 'series_id_example' # str | Series ID to filter. If not specified, will return all series. (optional)
    start = optimeering_beta.Start() # Start | The first datetime to fetch (inclusive). Defaults to current time. Should be specified in ISO 8601 datetime or duration format (eg - '2024-05-15T06:00:00+00:00', 'P1H', '-P1W1D', etc.) (optional)
    end = optimeering_beta.End() # End | The last datetime to fetch (exclusive). Defaults to 2099-12-30. Should be specified in ISO 8601 datetime or duration format (eg - '2024-05-15T06:00:00+00:00', 'P1H', '-P1W1D', etc.) (optional)
    limit = 2 # int | Number of items per page (optional)
    offset = 56 # int | Page offset (optional)

    try:
        # Get Predictions
        api_response = api_instance.get_predictions(series_id=series_id, start=start, end=end, limit=limit, offset=offset)
        print("The response of PredictionsApi->get_predictions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PredictionsApi->get_predictions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **series_id** | **str**| Series ID to filter. If not specified, will return all series. | [optional] 
 **start** | [**Start**](.md)| The first datetime to fetch (inclusive). Defaults to current time. Should be specified in ISO 8601 datetime or duration format (eg - &#39;2024-05-15T06:00:00+00:00&#39;, &#39;P1H&#39;, &#39;-P1W1D&#39;, etc.) | [optional] 
 **end** | [**End**](.md)| The last datetime to fetch (exclusive). Defaults to 2099-12-30. Should be specified in ISO 8601 datetime or duration format (eg - &#39;2024-05-15T06:00:00+00:00&#39;, &#39;P1H&#39;, &#39;-P1W1D&#39;, etc.) | [optional] 
 **limit** | **int**| Number of items per page | [optional] 
 **offset** | **int**| Page offset | [optional] 

### Return type

[**PredsDataGetResponse**](PredsDataGetResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

