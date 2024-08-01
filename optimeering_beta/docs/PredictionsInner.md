# PredictionsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prediction_for** | **datetime** | The time prediction is made for.&#39; | 
**values** | **Dict[str, float]** |  | 
**value** | **float** |  | 

## Example

```python
from optimeering_beta.models.predictions_inner import PredictionsInner

# TODO update the JSON string below
json = "{}"
# create an instance of PredictionsInner from a JSON string
predictions_inner_instance = PredictionsInner.from_json(json)
# print the JSON string representation of the object
print(PredictionsInner.to_json())

# convert the object into a dict
predictions_inner_dict = predictions_inner_instance.to_dict()
# create an instance of PredictionsInner from a dict
predictions_inner_from_dict = PredictionsInner.from_dict(predictions_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


