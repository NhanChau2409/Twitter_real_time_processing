from pyspark import SparkContext
from pyspark.sql import SparkSession 
from pyspark.streaming import StreamingContext
import json
from datetime import datetime
from pyspark.sql import functions


# Initiate pyspark streaming class with 10 second batch interval
spark = (SparkSession
         .builder
         .master("local[*]")
         .appName("SocketStream")
         .getOrCreate())

socketDF = (spark.readStream
            .format('socket')
            .option('host', "127.0.0.1")
            .option('port', 5555)
            .load())
# Schema StructType([StructField('value', StringType(), True)])

q = socketDF.agg(functions.count("*").alias("count"))

query1 = (q
    .writeStream
    .format("console")
    .outputMode("complete")
    .start()
    .awaitTermination())






