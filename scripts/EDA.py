import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.sql.types import IntegerType

from pyspark.sql.functions import date_format, to_date, dayofweek, from_unixtime, avg


spark = SparkSession.builder\
    .appName("BDT Project")\
    .master("local[*]")\
    .config("hive.metastore.uris", "thrift://sandbox-hdp.hortonworks.com:9083")\
    .config("spark.sql.catalogImplementation","hive")\
    .config("spark.sql.avro.compression.codec", "snappy")\
    .config("spark.jars", "file:///usr/hdp/current/hive-client/lib/hive-metastore-1.2.1000.2.6.5.0-292.jar,file:///usr/hdp/current/hive-client/lib/hive-exec-1.2.1000.2.6.5.0-292.jar")\
    .config("spark.jars.packages","org.apache.spark:spark-avro_2.12:3.0.3")\
    .enableHiveSupport()\
    .getOrCreate()


sc = spark.sparkContext

# print(sc)


# print(spark.catalog.listDatabases())

# print(spark.catalog.listTables("projectdb"))

trips = spark.read.format("avro").table('projectdb.trips')
trips.createOrReplaceTempView('trips')


trips.printSchema()

print("\n\n Process Date \n\n")

# convert timestamp from bigint to timestamp
trips = trips.withColumn('timestamp', from_unixtime(trips['timestamp']))

# add new columns for year, month, day, hour, and day of the week
trips = trips.withColumn('year', date_format('timestamp', 'y')) \
    .withColumn('month', date_format('timestamp', 'M')) \
    .withColumn('day', date_format('timestamp', 'd')) \
    .withColumn('hour', date_format('timestamp', 'H')) \
    .withColumn('day_of_week', dayofweek(to_date('timestamp'))) 



print("\n\n Process Polyline \n\n")

trips = trips.drop("polyline == []")
trips = trips.filter("missing_data == false")


polyline_length_udf = F.udf(lambda x: len(x.split('],'))-1, IntegerType())
trip_time_sec_udf = F.udf(lambda x: (len(x.split('],'))-1)*15, IntegerType())

# Add a new column with the trip time sec
trips = trips.withColumn('polyline_length', polyline_length_udf(trips['POLYLINE']))
trips = trips.withColumn('trip_time_sec', trip_time_sec_udf(trips['POLYLINE']))


# Show the first few rows of the DataFrame
trips.show(5)

# EXTRACT INSIGHTS

avg_trip_time_by_dow = trips.groupBy('day_of_week').agg(avg('trip_time_sec').alias('avg_trip_time'))
avg_trip_time_by_dow = avg_trip_time_by_dow.orderBy('day_of_week')
avg_trip_time_by_dow.show()