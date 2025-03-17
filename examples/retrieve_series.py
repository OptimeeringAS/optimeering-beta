from optimeering_beta import OptimeeringClient

client = OptimeeringClient()

series = client.predictions_api.list_series(product=["Imbalance"], area=["NO1"], statistic=["Point"], unit_type=["Price_Spread"])
data = series.retrieve(start="-P1W")

df = data.to_pandas(unpack_value_method="new_rows")

print(df.head())