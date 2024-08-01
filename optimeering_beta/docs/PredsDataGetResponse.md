# PredsDataGetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[PredsSingleSeriesDataCreated]**](PredsSingleSeriesDataCreated.md) |  | 
**next_page** | **str** | The next page of results (if available). | [optional] 

## Example

```python
from optimeering_beta.models.preds_data_get_response import PredsDataGetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PredsDataGetResponse from a JSON string
preds_data_get_response_instance = PredsDataGetResponse.from_json(json)
# print the JSON string representation of the object
print(PredsDataGetResponse.to_json())

# convert the object into a dict
preds_data_get_response_dict = preds_data_get_response_instance.to_dict()
# create an instance of PredsDataGetResponse from a dict
preds_data_get_response_from_dict = PredsDataGetResponse.from_dict(preds_data_get_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


