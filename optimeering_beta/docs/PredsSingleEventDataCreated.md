# PredsSingleEventDataCreated


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** | The timestamp at which datapoint was registered | 
**event_time** | **datetime** | Timestamp for when datapoint was generated. | 
**id** | **int** | Unique Identifier for the resource type. | 
**predictions** | [**List[PredictionsInner]**](PredictionsInner.md) |  | 

## Example

```python
from optimeering_beta.models.preds_single_event_data_created import PredsSingleEventDataCreated

# TODO update the JSON string below
json = "{}"
# create an instance of PredsSingleEventDataCreated from a JSON string
preds_single_event_data_created_instance = PredsSingleEventDataCreated.from_json(json)
# print the JSON string representation of the object
print(PredsSingleEventDataCreated.to_json())

# convert the object into a dict
preds_single_event_data_created_dict = preds_single_event_data_created_instance.to_dict()
# create an instance of PredsSingleEventDataCreated from a dict
preds_single_event_data_created_from_dict = PredsSingleEventDataCreated.from_dict(preds_single_event_data_created_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


