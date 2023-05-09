import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.sql.types import IntegerType

from pyspark.sql.functions import date_format, to_date, dayofweek, from_unixtime, avg, count, when, col, max, min


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


print("\n\n Process Polyline \n\n")

trips = trips.filter("missing_data == false")

polyline_length_udf = F.udf(lambda x: len(x.split('],'))-1, IntegerType())
trip_time_sec_udf = F.udf(lambda x: (len(x.split('],'))-1)*15, IntegerType())

# Add a new column with the trip time sec
trips = trips.withColumn('polyline_length', polyline_length_udf(trips['POLYLINE']))
trips = trips.withColumn('trip_time_sec', trip_time_sec_udf(trips['POLYLINE']))

# drop where trip time in sec is zero
trips = trips.where(trips.trip_time_sec != 0)

# Show the first few rows of the DataFrame
trips.show(5)


print("\n\n Polyline Length and Call Type as features \n\n")

from pyspark.sql.functions import col
from pyspark.ml.feature import OneHotEncoder, VectorAssembler
from pyspark.ml.linalg import Vectors
from pyspark.ml import Pipeline

# create example dataframe with 'category' column

# create OneHotEncoderEstimator
encoder = OneHotEncoder(inputCols=["call_type"],
                        outputCols=["call_type_vec"])

assembler = VectorAssembler(
    inputCols=["polyline_length", "call_type_vec"],
    outputCol="features")

pipeline = Pipeline(stages=[encoder, assembler])

# fit and transform dataframe
pipeline_model = pipeline.fit(trips)
trips_preprocessed = pipeline_model.transform(trips)

# show encoded dataframe
trips_preprocessed.show()


# Select features
X = trips_preprocessed.select('features')
y = trips_preprocessed.select('trip_time_sec')

# Train-Test split
train_data, test_data = trips_preprocessed.randomSplit([0.7, 0.3], seed=1337)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL 1 - Linear Regression

from pyspark.ml.regression import LinearRegression, RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.feature import VectorAssembler


print("\n\n MODEL 1 - Linear Regression \n\n")


# define the model
lr = LinearRegression()

# define the grid of hyperparameters to search
param_grid = ParamGridBuilder() \
    .addGrid(lr.regParam, [0.01, 0.1, 1.0]) \
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0]) \
    .build()

# define the evaluator to use
evaluator = RegressionEvaluator(metricName="rmse", labelCol="label")

# define the cross-validator to use
cv = CrossValidator(estimator=lr, estimatorParamMaps=param_grid, evaluator=evaluator, numFolds=4)

# fit the model using the cross-validator
cv_model = cv.fit(train_data)

# get the best model from the cross-validator
best_model = cv_model.bestModel

# evaluate the best model on the test data
# test_data = ...
predictions = best_model.transform(test_data)
rmse = evaluator.evaluate(predictions)
r2 = evaluator.evaluate(predictions, {evaluator.metricName: "r2"})


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL 2 - Random Forest

print("\n\n MODEL 2 - Random Forest \n\n")

rf = RandomForestRegressor()

# define the grid of hyperparameters to search
param_grid = ParamGridBuilder() \
    .addGrid(rf.maxDepth, [2, 4, 6]) \
    .addGrid(rf.numTrees, [10, 50, 100]) \
    .build()

# define the evaluator to use
evaluator = RegressionEvaluator(metricName="rmse", labelCol="label")

# define the cross-validator to use
cv = CrossValidator(estimator=rf, estimatorParamMaps=param_grid, evaluator=evaluator, numFolds=4)

# fit the model using the cross-validator
cv_model = cv.fit(train_data)

# get the best model from the cross-validator
best_model = cv_model.bestModel

# evaluate the best model on the test data
# test_data = ...
predictions = best_model.transform(test_data)
rmse = evaluator.evaluate(predictions)
r2 = evaluator.evaluate(predictions, {evaluator.metricName: "r2"})