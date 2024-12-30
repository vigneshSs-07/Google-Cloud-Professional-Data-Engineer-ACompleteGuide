import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import BooleanType

if len(sys.argv) == 1:
    print("Please provide a GCS bucket name.")

BUCKET = sys.argv[1]
print("The bucket name passed is ",BUCKET)
table = "bigquery-public-data:new_york_citibike.citibike_trips"
bucket_path = (f"gs://{BUCKET}/citibikes_top_ten_start_station_ids").format(BUCKET)
print("The bucket path where file will be written", bucket_path)

spark = SparkSession.builder \
          .appName("pyspark-example") \
          .config("spark.jars","gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar") \
          .getOrCreate()

df = spark.read.format("bigquery").load(table)

top_ten = df.filter(col("start_station_id") \
            .isNotNull()) \
            .groupBy("start_station_id") \
            .count() \
            .orderBy("count", ascending=False) \
            .limit(10) \
            .cache()

top_ten.show()

top_ten.write.mode("overwrite").option("header", True).csv(bucket_path)

