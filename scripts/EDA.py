import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline


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

print(sc)


print(spark.catalog.listDatabases())

print(spark.catalog.listTables("projectdb"))

trips = spark.read.format("avro").table('projectdb.trips')
trips.createOrReplaceTempView('trips')

trips.printSchema()
