from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType

from pyspark.sql.functions import date_format, to_date, dayofweek,\
    from_unixtime, avg, count, when, col


SPARK = SparkSession.builder\
    .appName("BDT Project")\
    .master("local[*]")\
    .config("hive.metastore.uris", "thrift://sandbox-hdp.hortonworks.com:9083")\
    .config("spark.sql.catalogImplementation", "hive")\
    .config("spark.sql.avro.compression.codec", "snappy")\
    .config("spark.jars", "file:///usr/hdp/current/hive-client/lib/"
                          "hive-metastore-1.2.1000.2.6.5.0-292.jar,file:///"
                          "usr/hdp/current/hive-client/lib/hive-exec-1.2.1000.2.6.5.0-292.jar")\
    .config("spark.jars.packages", "org.apache.spark:spark-avro_2.12:3.0.3")\
    .enableHiveSupport()\
    .getOrCreate()

TRIPS = SPARK.read.format("avro").table('projectdb.trips')
TRIPS.createOrReplaceTempView('trips')

TRIPS.printSchema()

print "\n\n Process Date \n\n"

# convert timestamp from bigint to timestamp
TRIPS = TRIPS.withColumn('timestamp', from_unixtime(TRIPS['timestamp']))

# add new columns for year, month, day, hour, and day of the week
TRIPS = TRIPS.withColumn('year', date_format('timestamp', 'y')) \
    .withColumn('month', date_format('timestamp', 'M')) \
    .withColumn('day', date_format('timestamp', 'd')) \
    .withColumn('hour', date_format('timestamp', 'H')) \
    .withColumn('day_of_week', dayofweek(to_date('timestamp')))

print "\n\n Process Polyline \n\n"

TRIPS = TRIPS.filter("missing_data == false")
TRIPS = TRIPS.withColumn('trip_time_sec', TRIPS['trip_time_sec'].cast(IntegerType()))

POLYLINE_LENGTH_UDF = F.udf(lambda x: len(x.split('],'))-1, IntegerType())

# Add a new column with the trip time sec
TRIPS = TRIPS.withColumn('polyline_length', POLYLINE_LENGTH_UDF(TRIPS['POLYLINE']))

# drop where trip time in sec is zero
TRIPS = TRIPS.where(TRIPS.trip_time_sec != 0)

# Show the first few rows of the DataFrame
TRIPS.show(5)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXTRACT INSIGHTS

print "\n\n Extract Insights \n\n"

CSV_DIR = 'output'

TRIPS = TRIPS.withColumn('timestamp', TRIPS['timestamp'].cast(StringType()))
TRIPS.sample(fraction=0.01, seed=1337).write.csv("%s/trips_preprocessed" % CSV_DIR)


MISSING_VALS = TRIPS.select([count(when(col(c).isNull(), c)).alias(c) for c in TRIPS.columns])
MISSING_VALS.show()
print "Missing values\n\n"
# columns: trip_id,call_type,origin_call,origin_stand,taxi_id,timestamp,
# day_type,missing_data,polyline,year,month,day,hour,day_of_week,polyline_length,trip_time_sec
MISSING_VALS.write.csv("%s/q1" % CSV_DIR)

AVG_TRIP_TIME_BY_DOW = TRIPS.groupBy('day_of_week').agg(avg('trip_time_sec').alias('avg_trip_time'))
AVG_TRIP_TIME_BY_DOW = AVG_TRIP_TIME_BY_DOW.orderBy('day_of_week')
AVG_TRIP_TIME_BY_DOW.show()
print "Day of week\n\n"
# columns: day_of_week,avg_trip_time
AVG_TRIP_TIME_BY_DOW.write.csv("%s/q2" % CSV_DIR)


AVG_TRIP_TIME_BY_H = TRIPS.groupBy('hour').agg(avg('trip_time_sec').alias('avg_trip_time'))
AVG_TRIP_TIME_BY_H = AVG_TRIP_TIME_BY_H.orderBy('hour')
AVG_TRIP_TIME_BY_H.show()
print "Hours\n\n"
# columns: hour,avg_trip_time
AVG_TRIP_TIME_BY_H.write.csv("%s/q3" % CSV_DIR)



AVG_TRIP_TIME_BY_CALL_T = TRIPS.groupBy('call_type').\
    agg(avg('trip_time_sec').alias('avg_trip_time'))
AVG_TRIP_TIME_BY_CALL_T.show()
print "call type (avg)\n\n"
# columns: call_type,avg_trip_time
AVG_TRIP_TIME_BY_CALL_T.write.csv("%s/q4" % CSV_DIR)


COUNT_TRIP_TIME_BY_CALL_T = TRIPS.groupBy('call_type').\
    agg(count('trip_time_sec').alias('count_trip_time'))
COUNT_TRIP_TIME_BY_CALL_T.show()
print "call type (count)\n\n"
# columns: call_type,count_trip_time
COUNT_TRIP_TIME_BY_CALL_T.write.csv("%s/q5" % CSV_DIR)


# assuming that `trips` is the name of the DataFrame that contains the `trip_time_sec` column
MIN_MAX_AVG = TRIPS.agg(avg('trip_time_sec').alias('avg_trip_time'),
                        F.max('trip_time_sec').alias('max_trip_time'),
                        F.min('trip_time_sec').alias('min_trip_time'))
MIN_MAX_AVG.show()
print "avg, max, min\n\n"
# columns: avg_trip_time,max_trip_time,min_trip_time
MIN_MAX_AVG.write.csv("%s/q6" % CSV_DIR)

DAY_TYPE_COUNT = TRIPS.groupBy('day_type').count()
DAY_TYPE_COUNT.show()
print "day type count\n\n"
# columns: day_type,count
DAY_TYPE_COUNT.write.csv("%s/q7" % CSV_DIR)
