# PredictionFloatModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prediction_for** | **datetime** | The time prediction is made for.&#39; | 
**value** | **float** |  | 

## Example

```python
from optimeering_beta.models.prediction_float_model import PredictionFloatModel

# TODO update the JSON string below
json = "{}"
# create an instance of PredictionFloatModel from a JSON string
prediction_float_model_instance = PredictionFloatModel.from_json(json)
# print the JSON string representation of the object
print(PredictionFloatModel.to_json())

# convert the object into a dict
prediction_float_model_dict = prediction_float_model_instance.to_dict()
# create an instance of PredictionFloatModel from a dict
prediction_float_model_from_dict = PredictionFloatModel.from_dict(prediction_float_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


