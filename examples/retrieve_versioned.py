from optimeering_beta import OptimeeringClient

client = OptimeeringClient()

versioned_series = client.predictions_api.list_version(product=["Imbalance"], area=["NO1"], statistic=["Point"], unit_type=["Price_Spread"])

# Example of how to find the last two versions for this series
versions = [s.version for s in versioned_series.items]
versions.sort(key=lambda s: list(map(int, s.split('.'))))
last_two_versions = versions[-2:]


filtered_versioned_series = versioned_series.filter(version=last_two_versions)

data = client.predictions_api.retrieve_versioned(versioned_series=filtered_versioned_series, start="-P1M", include_simulated=True)

df = data.to_pandas(unpack_value_method="new_rows")

print(df.head())