from optimeering_beta import OptimeeringClient

client = OptimeeringClient()

versioned_series = client.predictions_api.list_version(product=["Imbalance"], area=["NO1"], statistic=["Point"], unit_type=["Price_Spread"])
filtered_versions = versioned_series.filter(version=["1.2.1"])
data = filtered_versions.retrieve_versioned(start="-P1M", include_simulated=True)

df = data.to_pandas(unpack_value_method="new_rows")

print(df.head())