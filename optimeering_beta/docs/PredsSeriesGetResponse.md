# PredsSeriesGetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[PredsCreatedSeries]**](PredsCreatedSeries.md) |  | 
**next_page** | **str** | The next page of results (if available). | [optional] 

## Example

```python
from optimeering_beta.models.preds_series_get_response import PredsSeriesGetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PredsSeriesGetResponse from a JSON string
preds_series_get_response_instance = PredsSeriesGetResponse.from_json(json)
# print the JSON string representation of the object
print(PredsSeriesGetResponse.to_json())

# convert the object into a dict
preds_series_get_response_dict = preds_series_get_response_instance.to_dict()
# create an instance of PredsSeriesGetResponse from a dict
preds_series_get_response_from_dict = PredsSeriesGetResponse.from_dict(preds_series_get_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


