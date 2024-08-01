# PredsCreatedSeries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**area** | **str** | Areas to be filtered. E.g. NO1, NO2 | 
**created_at** | **datetime** |  | 
**description** | **str** |  | [optional] 
**id** | **int** |  | 
**latest_event_time** | **datetime** |  | [optional] 
**market** | **str** | Market type for the series | 
**name** | **str** | Unique name for the series | 
**statistic** | **str** | Type of statistics. | 
**unit_type** | **str** | Unit type for the series | 

## Example

```python
from optimeering_beta.models.preds_created_series import PredsCreatedSeries

# TODO update the JSON string below
json = "{}"
# create an instance of PredsCreatedSeries from a JSON string
preds_created_series_instance = PredsCreatedSeries.from_json(json)
# print the JSON string representation of the object
print(PredsCreatedSeries.to_json())

# convert the object into a dict
preds_created_series_dict = preds_created_series_instance.to_dict()
# create an instance of PredsCreatedSeries from a dict
preds_created_series_from_dict = PredsCreatedSeries.from_dict(preds_created_series_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


