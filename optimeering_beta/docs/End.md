# End

The last datetime to fetch (exclusive). Defaults to 2099-12-30. Should be specified in ISO 8601 datetime or duration format (eg - '2024-05-15T06:00:00+00:00', 'P1H', '-P1W1D', etc.)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from optimeering_beta.models.end import End

# TODO update the JSON string below
json = "{}"
# create an instance of End from a JSON string
end_instance = End.from_json(json)
# print the JSON string representation of the object
print(End.to_json())

# convert the object into a dict
end_dict = end_instance.to_dict()
# create an instance of End from a dict
end_from_dict = End.from_dict(end_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


