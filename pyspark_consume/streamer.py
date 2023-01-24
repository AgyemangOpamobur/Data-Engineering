# Read from kafka comnsumer
# Peform dataframe transformation
# Sink to Postgres JDBC

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time
from decimal import Decimal
from pyspark.sql.types import DecimalType

import numpy as np

from consume.foreachatch import foreach_batch_function
from consume.database import engine
from consume import models

# create the temperature_reading table
models.Base.metadata.create_all(bind=engine)


kafka_topic_name = "Environment-Readings"

kafka_bootstrap_servers = "kafka:9092"

if __name__ == "__main__":
    spark = SparkSession.builder\
        .appName("Kafka Pyspark Streamin Learning")\
            .master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
   
    posts_df = spark.readStream.format("kafka")\
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers)\
            .option("subscribe", kafka_topic_name)\
                .option("startingOffsets", "latest")\
                    .load()
    posts_df.printSchema()

    # setting precision to format the columns to 2dp
    Precision = 5
    Scale = 2    

    posts_df1 = posts_df.selectExpr("CAST(value as STRING)", "timestamp")
    posts_schema = StructType() \
        .add("id", StringType())\
                .add("ts", StringType())\
                    .add("device", StringType())\
                        .add("co", DecimalType(Precision,Scale))\
                            .add("humidity", DecimalType(Precision,Scale))\
                                .add("light", StringType())\
                                    .add("lpg", DecimalType(Precision,Scale))\
                                        .add("motion", StringType())\
                                            .add("smoke", DecimalType(Precision,Scale))\
                                                .add("temp", DecimalType(Precision, Scale))\

    posts_df2 = posts_df1.select(from_json(col("value"), posts_schema)\
        .alias("posts"), "timestamp")
    # posts_df2.printSchema()

    # convert temperature to fahrenheit
    def Fahrenheit():        
      celsius = np.array(posts_df2['posts.temp'])
      fahrenheit = (celsius * 9/5) + 32
      return fahrenheit
    # posts_df2['posts.temp'] = fahrenheit

    posts_df3 = posts_df2.select("posts.*", "timestamp")
    posts_df3.writeStream.outputMode("append").format('console').start()
    posts_df4 = posts_df3.groupBy("timestamp")\
        .agg({"temp": "count"}).alias("posts")
    posts_df5 = posts_df3.groupBy("ts").agg({"ts":"count"}).alias("ts_count")
    # posts_df4.printSchema()
    
    # posts_time = posts_df3.groupBy(year('ts')).agg({"temp":"count"}).alias("Fahrenheit")


    posts_stream = posts_df4.writeStream.trigger(processingTime='10 seconds')\
        .outputMode('update')\
            .option("truncate", "false")\
                .format("console")\
                    .start()
    
    posts_stream.awaitTermination()
    
    # dataframe to save to PostgreSQL
    df_final = posts_df1.select(
        "temp",
        col("id").alias("log_id"),
        col("ts").alias("ts"),
        col("device").alias("device"),
        col("co").alias("carbon"),
        col("humidity").alias("humidity"),
        col("light").alias("light"),
        col("lpg").alias("lpg"),
        col("motion").alias("motion"),
        col("smoke").alias("smoke"),
        col("temp").alias("temperature"),
        col("timestamp").alias("timestamp")).orderBy(asc("log_id"))
        # .orderBy(asc("temp"), asc("ts"))

    query = df_final\
        .writeStream.outputMode("complete").format("jdbc")\
        .foreachBatch(foreach_batch_function).start()

    query.awaitTermination()






