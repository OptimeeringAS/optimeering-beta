# PredsSingleSeriesDataCreated


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**events** | [**List[PredsSingleEventDataCreated]**](PredsSingleEventDataCreated.md) |  | 
**series_id** | **int** | Identifier for the series id. | 

## Example

```python
from optimeering_beta.models.preds_single_series_data_created import PredsSingleSeriesDataCreated

# TODO update the JSON string below
json = "{}"
# create an instance of PredsSingleSeriesDataCreated from a JSON string
preds_single_series_data_created_instance = PredsSingleSeriesDataCreated.from_json(json)
# print the JSON string representation of the object
print(PredsSingleSeriesDataCreated.to_json())

# convert the object into a dict
preds_single_series_data_created_dict = preds_single_series_data_created_instance.to_dict()
# create an instance of PredsSingleSeriesDataCreated from a dict
preds_single_series_data_created_from_dict = PredsSingleSeriesDataCreated.from_dict(preds_single_series_data_created_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


