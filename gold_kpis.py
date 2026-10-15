# Gold Layer - KPIs Calculation

df_silver = spark.read.table("silver_returns_cleaned")

# Gold KPIs Table
df_gold_kpis = df_silver.groupBy().agg(
    {"return_amount": "sum", "is_flagged": "sum"}
)

# Gold Product-wise Analysis
df_gold_product = df_silver.groupBy("product_name", "data_quality_flag").count()

df_gold_product.write.format("delta").mode("overwrite").saveAsTable("gold_returns_by_product")
