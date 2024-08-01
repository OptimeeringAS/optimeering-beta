# Start

The first datetime to fetch (inclusive). Defaults to current time. Should be specified in ISO 8601 datetime or duration format (eg - '2024-05-15T06:00:00+00:00', 'P1H', '-P1W1D', etc.)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from optimeering_beta.models.start import Start

# TODO update the JSON string below
json = "{}"
# create an instance of Start from a JSON string
start_instance = Start.from_json(json)
# print the JSON string representation of the object
print(Start.to_json())

# convert the object into a dict
start_dict = start_instance.to_dict()
# create an instance of Start from a dict
start_from_dict = Start.from_dict(start_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


