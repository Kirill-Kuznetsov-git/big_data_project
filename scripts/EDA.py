from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, LongType

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

trips = SPARK.read.format("avro").table('projectdb.trips')
trips.createOrReplaceTempView('trips')

trips.printSchema()

print "\n\n Process Date \n\n"

# convert timestamp from bigint to timestamp
trips = trips.withColumn('timestamp', from_unixtime(trips['timestamp']))

# add new columns for year, month, day, hour, and day of the week
trips = trips.withColumn('year', date_format('timestamp', 'y')) \
    .withColumn('month', date_format('timestamp', 'M')) \
    .withColumn('day', date_format('timestamp', 'd')) \
    .withColumn('hour', date_format('timestamp', 'H')) \
    .withColumn('day_of_week', dayofweek(to_date('timestamp')))

print "\n\n Process Polyline \n\n"

trips = trips.filter("missing_data == false")
trips = trips.withColumn('trip_time_sec', trips['trip_time_sec'].cast(IntegerType()))

polyline_length_udf = F.udf(lambda x: len(x.split('],'))-1, IntegerType())

# Add a new column with the trip time sec
trips = trips.withColumn('polyline_length', polyline_length_udf(trips['POLYLINE']))

# drop where trip time in sec is zero
trips = trips.where(trips.trip_time_sec != 0)

# Show the first few rows of the DataFrame
trips.show(5)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXTRACT INSIGHTS

print "\n\n Extract Insights \n\n"

csv_dir = 'output'


# We can get these in dashboard step

# # "Data Size: The total number of records or rows in the dataset"
# data_size_csv = ('data_size,\n%f' % (trips.count()))
# with open("%s/data_size.csv"%(csv_dir), "w") as file:
#     file.write(data_size_csv)

# # Data Distribution: The distribution of data across different categories or variables.
# data_size_csv = ('trip_id,call_type,origin_call,origin_stand,taxi_id,timestamp,day_type,missing_data,polyline,trip_time_sec\nLongType,StringType,DoubleType,DoubleType,IntegerType,LongType,StringType,BooleanType,StringType,IntegerType')
# with open("%s/data_type.csv"%(csv_dir), "w") as file:
#     file.write(data_size_csv)

trips = trips.withColumn('timestamp', trips['timestamp'].cast(LongType()))
trips.write.csv("%s/trips_preprocessed" % csv_dir)



missing_vals = trips.select([count(when(col(c).isNull(), c)).alias(c) for c in trips.columns])
missing_vals.show()
print "Missing values\n\n"
# columns: trip_id,call_type,origin_call,origin_stand,taxi_id,timestamp,
# day_type,missing_data,polyline,year,month,day,hour,day_of_week,polyline_length,trip_time_sec
missing_vals.write.csv("%s/q1" % csv_dir)

avg_trip_time_by_dow = trips.groupBy('day_of_week').agg(avg('trip_time_sec').alias('avg_trip_time'))
avg_trip_time_by_dow = avg_trip_time_by_dow.orderBy('day_of_week')
avg_trip_time_by_dow.show()
print "Day of week\n\n"
# columns: day_of_week,avg_trip_time
avg_trip_time_by_dow.write.csv("%s/q2" % csv_dir)


avg_trip_time_by_h = trips.groupBy('hour').agg(avg('trip_time_sec').alias('avg_trip_time'))
avg_trip_time_by_h = avg_trip_time_by_h.orderBy('hour')
avg_trip_time_by_h.show()
print "Hours\n\n"
# columns: hour,avg_trip_time
avg_trip_time_by_h.write.csv("%s/q3" % csv_dir)



avg_trip_time_by_call_t = trips.groupBy('call_type').\
    agg(avg('trip_time_sec').alias('avg_trip_time'))
avg_trip_time_by_call_t.show()
print "call type (avg)\n\n"
# columns: call_type,avg_trip_time
avg_trip_time_by_call_t.write.csv("%s/q4" % csv_dir)


count_trip_time_by_call_t = trips.groupBy('call_type').\
    agg(count('trip_time_sec').alias('count_trip_time'))
count_trip_time_by_call_t.show()
print "call type (count)\n\n"
# columns: call_type,count_trip_time
count_trip_time_by_call_t.write.csv("%s/q5" % csv_dir)


# assuming that `trips` is the name of the DataFrame that contains the `trip_time_sec` column
min_max_avg = trips.agg(avg('trip_time_sec').alias('avg_trip_time'),
                        F.max('trip_time_sec').alias('max_trip_time'),
                        F.min('trip_time_sec').alias('min_trip_time'))
min_max_avg.show()
print "avg, max, min\n\n"
# columns: avg_trip_time,max_trip_time,min_trip_time
min_max_avg.write.csv("%s/q6" % csv_dir)

day_type_count = trips.groupBy('day_type').count()
day_type_count.show()
print "day type count\n\n"
# columns: day_type,count
day_type_count.write.csv("%s/q7" % csv_dir)
