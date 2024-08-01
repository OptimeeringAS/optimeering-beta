# PredictionDictResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prediction_for** | **datetime** | The time prediction is made for.&#39; | 
**values** | **Dict[str, float]** |  | 

## Example

```python
from optimeering_beta.models.prediction_dict_response import PredictionDictResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PredictionDictResponse from a JSON string
prediction_dict_response_instance = PredictionDictResponse.from_json(json)
# print the JSON string representation of the object
print(PredictionDictResponse.to_json())

# convert the object into a dict
prediction_dict_response_dict = prediction_dict_response_instance.to_dict()
# create an instance of PredictionDictResponse from a dict
prediction_dict_response_from_dict = PredictionDictResponse.from_dict(prediction_dict_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


