# optimeering_beta.ParametersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_parameter_values**](ParametersApi.md#get_parameter_values) | **GET** /api/parameters/{param} | Parameter List


# **get_parameter_values**
> object get_parameter_values(param)

Parameter List

### Example


```python
import optimeering_beta
from optimeering_beta.models.enum_parameters import EnumParameters
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
    api_instance = optimeering_beta.ParametersApi(api_client)
    param = optimeering_beta.EnumParameters() # EnumParameters | 

    try:
        # Parameter List
        api_response = api_instance.get_parameter_values(param)
        print("The response of ParametersApi->get_parameter_values:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ParametersApi->get_parameter_values: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **param** | [**EnumParameters**](.md)|  | 

### Return type

**object**

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

