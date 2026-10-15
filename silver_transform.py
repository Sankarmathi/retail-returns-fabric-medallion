# Retail Returns - Silver Layer Transformation
# Microsoft Fabric - PySpark Notebook

from pyspark.sql.functions import when, col

# 1. Read Bronze layer data
df_bronze = spark.read.format("delta").load("Tables/bronze_returns")

# 2. Silver Layer - Data Cleaning & Quality Flag Logic
df_silver = df_bronze.withColumn(
    "data_quality_flag",
    when(col("return_amount") > col("cost_price"), "OVER-REFUND")
    .when((col("cost_price") == 0) | (col("return_amount") == 0.60), "DATA ERROR")
    .when(col("warehouse") == "UNKNOWN", "MISSING INVENTORY")
    .otherwise("CLEAN")
).withColumn(
    "is_flagged", col("data_quality_flag") != "CLEAN"
)

# 3. Write to Silver Delta Table
df_silver.write.format("delta").mode("overwrite").saveAsTable("silver_returns_cleaned")

# 4. Show flagged records for verification
df_silver.filter(col("is_flagged") == True).show()
