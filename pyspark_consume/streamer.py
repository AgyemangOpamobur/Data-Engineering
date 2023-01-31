# Read from kafka comnsumer
# Peform dataframe transformation
# Sink to Postgres JDBC

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from decimal import Decimal
from pyspark.sql.types import DecimalType
from consume.foreachbatch import foreach_batch_function
from consume.database import engine
from consume import models

#funtion to convert celsuis to Fah...


def Fahrenheit(df):
    return df.withColumn(
        "temp_fa", round((df.temperature*9/5) + 32, 2))


# create the environmental_readings table
models.Base.metadata.create_all(bind=engine)


kafka_topic_name = "Environment-Readings"

kafka_bootstrap_servers = "kafka:9092"

if __name__ == "__main__":
    spark = SparkSession.builder\
        .appName("Kafka Pyspark Streaming Learning")\
        .master("local[2]")\
        .config("spark.jars", "postgresql-42.4.0.jar").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    posts_df = spark.readStream.format("kafka")\
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers)\
        .option("subscribe", kafka_topic_name)\
        .option("startingOffsets", "latest")\
        .load()

    # posts_df.printSchema()

    # setting precision to format the columns to 2dp
    Precision = 5
    Scale = 2

    posts_df1 = posts_df.selectExpr(
        "CAST(key AS STRING)", "CAST(value AS STRING)")

    posts_schema = StructType(fields=[
        StructField("id", StringType(), False),
        StructField("ts", StringType(), True),
        StructField("device", StringType(), True),
        StructField("co", StringType(), True),
        StructField("humidity", StringType(), True),
        StructField("light", StringType(), True),
        StructField("lpg", StringType(), True),
        StructField("motion", StringType(), True),
        StructField("smoke", StringType(), True),
        StructField("temp", StringType(), True)
    ])
    posts_df2 = posts_df1.select(
        from_json(posts_df1.value, posts_schema).alias("dataframe"))

    df_formatted = posts_df2.select(
        col("dataframe.id").alias("Id"),
        col("dataframe.ts").alias("ts"),
        col("dataframe.device").alias("device_id"),
        col("dataframe.co").alias("co"),
        col("dataframe.humidity").alias("humidity_level"),
        col("dataframe.light").alias("light"),
        col("dataframe.lpg").alias("lpg_level"),
        col("dataframe.motion").alias("motion"),
        col("dataframe.smoke").alias("smoke_conc"),
        col("dataframe.temp").alias("temperature")
    )
    # format dat types
    df = df_formatted.withColumn("Id", df_formatted.Id.cast(IntegerType()))
    df = df.withColumn("humidity_level", df.humidity_level.cast(
        DecimalType(Precision, Scale)))
    df = df.withColumn("temperature", df.temperature.cast(
        DecimalType(Precision, Scale)))

    # add column for current timestamp
    post_df_with_tmps = df.withColumn(
        "timestamp", current_timestamp())

    posts_df3 = post_df_with_tmps.transform(Fahrenheit)

    # Define  the window to perform transformation on the dataframe
    # I am subseting the columns here I don't think all the columns are relevant to me
    # I am performing the agrregation every 3 minutes
    # I am caluclating  the aveage temperature  and humidity for every device within the period
    df_window = (posts_df3.withWatermark("timestamp", "15 seconds")
                 .groupBy(window(posts_df3.timestamp, "15 seconds"), posts_df3.Id, posts_df3.device_id)
                 .avg("temp_fa", "humidity_level"))

    # dataframe to save to PostgreSQL
    df_final = df_window.select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("device_id"),
        col("avg(temp_fa)").alias("Fahrenheit"), col("avg(humidity_level)").alias("humidity")).orderBy(asc("Id"), asc("window_start"))

    query = df_final\
        .writeStream.outputMode("complete").format("jdbc")\
        .foreachBatch(foreach_batch_function).start()

    query.awaitTermination()
    
