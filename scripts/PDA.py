import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType

from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.regression import LinearRegression, RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator


spark = SparkSession.builder\
    .appName("BDT Project")\
    .master("local[*]")\
    .config("hive.metastore.uris", "thrift://sandbox-hdp.hortonworks.com:9083")\
    .config("spark.sql.catalogImplementation","hive")\
    .config("spark.sql.avro.compression.codec", "snappy")\
    .config("spark.jars", "file:///usr/hdp/current/hive-client/lib/hive-metastore-1.2.1000.2.6.5.0-292.jar,file:///usr/hdp/current/hive-client/lib/hive-exec-1.2.1000.2.6.5.0-292.jar")\
    .config("spark.jars.packages","org.apache.spark:spark-avro_2.12:3.0.3")\
    .config("spark.driver.memory", "32g") \
    .config("spark.executor.memory", "24g") \
    .enableHiveSupport()\
    .getOrCreate()


sc = spark.sparkContext

trips = spark.read.format("avro").table('projectdb.trips')
trips.createOrReplaceTempView('trips')
trips.printSchema()

print("\n\n Process Date \n\n")

# convert timestamp from bigint to timestamp
trips = trips.withColumn('timestamp', F.from_unixtime(trips['timestamp']))

# add new columns for year, month, day, hour, and day of the week
trips = trips.withColumn('year', F.date_format('timestamp', 'y')) \
    .withColumn('month', F.date_format('timestamp', 'M')) \
    .withColumn('day', F.date_format('timestamp', 'd')) \
    .withColumn('hour', F.date_format('timestamp', 'H')) \
    .withColumn('day_of_week', F.dayofweek(F.to_date('timestamp'))) 

print("\n\n Process Date \n\n")

# convert timestamp from bigint to timestamp
trips = trips.withColumn('timestamp', F.from_unixtime(trips['timestamp']))

# add new columns for year, month, day, hour, and day of the week
trips = trips.withColumn('year', F.date_format('timestamp', 'y').cast(IntegerType())) \
    .withColumn('month', F.date_format('timestamp', 'M').cast(IntegerType())) \
    .withColumn('day', F.date_format('timestamp', 'd').cast(IntegerType())) \
    .withColumn('hour', F.date_format('timestamp', 'H').cast(IntegerType())) \
    .withColumn('day_of_week', F.dayofweek(F.to_date('timestamp')).cast(IntegerType()))

print("\n\n Process Polyline \n\n")

trips = trips.filter("missing_data == false")

polyline_length_udf = F.udf(lambda x: len(x.split('],'))-1, IntegerType())
trip_time_sec_udf = F.udf(lambda x: (len(x.split('],'))-1)*15, IntegerType())

# Add a new column with the trip time sec
trips = trips.withColumn('polyline_length', polyline_length_udf(trips['POLYLINE']))
trips = trips.withColumn('trip_time_sec', trip_time_sec_udf(trips['POLYLINE']))

# drop where trip time in sec is zero
trips = trips.where(trips.trip_time_sec != 0)
# drop where null in hours or day of week
trips = trips.na.drop(subset=["hour","day_of_week"])

# Show the first few rows of the DataFrame
trips.show(5)


print("\n\n Polyline Length and Call Type as features \n\n")


# categorical feature label indexing
indexer = StringIndexer(inputCol="call_type", outputCol="call_type_index")

# create OneHotEncoderEstimator
encoder = OneHotEncoder(inputCols=["call_type_index"],
                        outputCols=["call_type_vec"])

assembler = VectorAssembler(
    inputCols=["polyline_length", "hour", "day_of_week", "call_type_vec"],
    outputCol="features")

pipeline = Pipeline(stages=[indexer, encoder, assembler])

# fit and transform dataframe
pipeline_model = pipeline.fit(trips)
trips_preprocessed = pipeline_model.transform(trips)

# show encoded dataframe
trips_preprocessed.show()


# Train-Test split
train_data, test_data = trips_preprocessed.randomSplit([0.7, 0.3], seed=1337)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL 1 - Linear Regression

print("\n\n MODEL 1 - Linear Regression \n\n")


# define the model
lr = LinearRegression(featuresCol="features", labelCol="trip_time_sec")

# define the grid of hyperparameters to search
param_grid = ParamGridBuilder() \
    .addGrid(lr.regParam, [0.01, 0.1, 1.0]) \
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0]) \
    .build()

# # define the evaluator to use
evaluator_rmse = RegressionEvaluator(metricName="rmse", labelCol="trip_time_sec")
evaluator_r2 = RegressionEvaluator(metricName="r2", labelCol="trip_time_sec")

# define the cross-validator to use
cv = CrossValidator(estimator=lr, estimatorParamMaps=param_grid, evaluator=evaluator_rmse, numFolds=4)

# fit the model using the cross-validator
cv_model = cv.fit(train_data)

# get the best model from the cross-validator
best_model = cv_model.bestModel

lr_predictions = best_model.transform(test_data)
lr_rmse = evaluator_rmse.evaluate(lr_predictions)
lr_r2 = evaluator_r2.evaluate(lr_predictions)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL 2 - Random Forest

print("\n\n MODEL 2 - Random Forest \n\n")

rf = RandomForestRegressor(featuresCol="features", labelCol="trip_time_sec")

# define the grid of hyperparameters to search
param_grid = ParamGridBuilder() \
    .addGrid(rf.maxDepth, [2, 4, 6]) \
    .addGrid(rf.numTrees, [10, 50, 100]) \
    .build()

# define the cross-validator to use
cv = CrossValidator(estimator=rf, estimatorParamMaps=param_grid, evaluator=evaluator_rmse, numFolds=4)

# fit the model using the cross-validator
cv_model = cv.fit(train_data)

# get the best model from the cross-validator
best_model = cv_model.bestModel

# evaluate the best model on the test data
rf_predictions = best_model.transform(test_data)
rf_rmse = evaluator_rmse.evaluate(rf_predictions)
rf_r2 = evaluator_r2.evaluate(rf_predictions)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# print metrics

print("METRICS:")
print("Linear Regression:")
print("\t- RMSE:", lr_rmse)
print("\t- R2:", lr_r2)
lr_predictions.select("trip_time_sec", "prediction").show()

print("Random Forest:")
print("\t- RMSE:", rf_rmse)
print("\t- R2:", rf_r2)
rf_predictions.select("trip_time_sec", "prediction").show()

csv_dir = 'output'

evaluation_csv = ('metic,lr,rf\nrmse,%f,%f\nr2,%f,%f' %(lr_rmse, rf_rmse, lr_r2, rf_r2))
open("%s/evaluation.csv"%(csv_dir), "w").write(evaluation_csv)

lr_predictions.select([F.col(c).cast("string") for c in lr_predictions.columns])
# columns: trip_id,call_type,origin_call,origin_stand,taxi_id,timestamp,day_type,missing_data,polyline,year,month,day,hour,day_of_week,polyline_length,trip_time_sec,call_type_index,call_type_vec,features
trips_preprocessed.write.csv("%s/pipeline_output" % csv_dir)

lr_predictions = lr_predictions.select("trip_time_sec", "prediction")
lr_predictions.select([F.col(c).cast("string") for c in lr_predictions.columns])
# columns: trip_id,call_type,origin_call,origin_stand,taxi_id,timestamp,day_type,missing_data,polyline,year,month,day,hour,day_of_week,polyline_length,trip_time_sec,call_type_index,call_type_vec,features,prediction
lr_predictions.write.csv("%s/lr" % csv_dir)

rf_predictions = rf_predictions.select("trip_time_sec", "prediction")
rf_predictions.select([F.col(c).cast("string") for c in lr_predictions.columns])
# columns: trip_id,call_type,origin_call,origin_stand,taxi_id,timestamp,day_type,missing_data,polyline,year,month,day,hour,day_of_week,polyline_length,trip_time_sec,call_type_index,call_type_vec,features,prediction
rf_predictions.write.csv("%s/rf" % csv_dir)
