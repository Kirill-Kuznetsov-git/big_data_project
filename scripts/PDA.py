"""Module providing PDA."""
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType

from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.regression import LinearRegression, RandomForestRegressor, GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator


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
    .config("spark.driver.memory", "32g") \
    .config("spark.executor.memory", "32g") \
    .enableHiveSupport()\
    .getOrCreate()


SC = SPARK.sparkContext

# decrease number of logs
SC.setLogLevel('WARN')

TRIPS = SPARK.read.format("avro").table('projectdb.trips')
TRIPS.createOrReplaceTempView('trips')
TRIPS.printSchema()

print "\n\n Process Date \n\n"

# convert timestamp from bigint to timestamp
TRIPS = TRIPS.withColumn('timestamp', F.from_unixtime(TRIPS['timestamp']))

# add new columns for year, month, day, hour, and day of the week
TRIPS = TRIPS.withColumn('year', F.date_format('timestamp', 'y')) \
    .withColumn('month', F.date_format('timestamp', 'M')) \
    .withColumn('day', F.date_format('timestamp', 'd')) \
    .withColumn('hour', F.date_format('timestamp', 'H')) \
    .withColumn('day_of_week', F.dayofweek(F.to_date('timestamp'))) 

# convert to int
TRIPS = TRIPS.withColumn('hour', TRIPS['hour'].cast(IntegerType())) \
    .withColumn('day_of_week', TRIPS['day_of_week'].cast(IntegerType()))


print "\n\n Process Polyline \n\n"

TRIPS = TRIPS.filter("missing_data == false")
TRIPS = TRIPS.withColumn('trip_time_sec', TRIPS['trip_time_sec'].cast(IntegerType()))

polyline_length_udf = F.udf(lambda x: len(x.split('],'))-1, IntegerType())

# Add a new column with the trip time sec
TRIPS = TRIPS.withColumn('polyline_length', polyline_length_udf(TRIPS['POLYLINE']))

# drop where trip time in sec is zero
TRIPS = TRIPS.where(TRIPS.trip_time_sec != 0)
# drop where null in hours or day of week
TRIPS = TRIPS.na.drop(subset=["hour","day_of_week"])

# Show the first few rows of the DataFrame
TRIPS.show(5)


print "\n\n Polyline Length and Call Type as features \n\n"


# categorical feature label indexing
INDEXER = StringIndexer(inputCol="call_type", outputCol="call_type_index")

# create OneHotEncoderEstimator
ENCODER = OneHotEncoder(inputCols=["call_type_index"],
                        outputCols=["call_type_vec"])

ASSEMBLER = VectorAssembler(
    inputCols=["polyline_length", "hour", "day_of_week", "call_type_vec"],
    outputCol="features")

PIPELINE = Pipeline(stages=[INDEXER, ENCODER, ASSEMBLER])

# fit and transform dataframe
PIPELINE_MODEL = PIPELINE.fit(TRIPS)
TRIPS_PREPROCESSED = PIPELINE_MODEL.transform(TRIPS)

# show encoded dataframe
TRIPS_PREPROCESSED.show()

# select only relevant columns for model
TRIPS_DATA = TRIPS_PREPROCESSED.select("features", "trip_time_sec")

# Train-Test split
TRAIN_DATA, TEST_DATA = TRIPS_DATA.randomSplit([0.7, 0.3], seed=1337)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL 1 - Linear Regression

def run_lr(train_data, test_data):
    print "\n\n MODEL 1 - Linear Regression \n\n"


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
    cv = CrossValidator(estimator=lr, estimatorParamMaps=param_grid,
                        evaluator=evaluator_rmse, numFolds=4)

    # fit the model using the cross-validator
    cv_model = cv.fit(train_data)

    # get the best model from the cross-validator
    best_model = cv_model.bestModel

    lr_predictions = best_model.transform(test_data)
    lr_rmse = evaluator_rmse.evaluate(lr_predictions)
    lr_r2 = evaluator_r2.evaluate(lr_predictions)

    best_model.save("models/LR")
    
    return lr_predictions, lr_rmse, lr_r2

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL 2 - Random Forest

def run_rf(train_data, test_data):
    print "\n\n MODEL 2 - Random Forest \n\n"

    rf = RandomForestRegressor(featuresCol="features", labelCol="trip_time_sec")

    # define the grid of hyperparameters to search
    param_grid = ParamGridBuilder() \
        .addGrid(rf.maxDepth, [2, 4, 6]) \
        .addGrid(rf.numTrees, [10, 50, 100]) \
        .build()

    # define the evaluator to use
    evaluator_rmse = RegressionEvaluator(metricName="rmse", labelCol="trip_time_sec")
    evaluator_r2 = RegressionEvaluator(metricName="r2", labelCol="trip_time_sec")


    # define the cross-validator to use
    cv = CrossValidator(estimator=rf, estimatorParamMaps=param_grid,
                        evaluator=evaluator_rmse, numFolds=4)

    # fit the model using the cross-validator
    cv_model = cv.fit(train_data)

    # get the best model from the cross-validator
    best_model = cv_model.bestModel

    # evaluate the best model on the test data
    rf_predictions = best_model.transform(test_data)
    rf_rmse = evaluator_rmse.evaluate(rf_predictions)
    rf_r2 = evaluator_r2.evaluate(rf_predictions)

    best_model.save("models/RF")

    return rf_predictions, rf_rmse, rf_r2

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL 3 - Gradient Boosted Tree
def run_gbt(train_data, test_data):
    print "\n\n MODEL 3 - Gradient Boosted Tree \n\n"

    gbt = GBTRegressor(featuresCol="features", labelCol="trip_time_sec")

    # Define the hyperparameter grid for tuning
    paramGrid = ParamGridBuilder() \
        .addGrid(gbt.maxDepth, [5, 10, 15]) \
        .addGrid(gbt.stepSize, [0.1, 0.05, 0.01]) \
        .build()

    # define the evaluator to use
    evaluator_rmse = RegressionEvaluator(metricName="rmse", labelCol="trip_time_sec")
    evaluator_r2 = RegressionEvaluator(metricName="r2", labelCol="trip_time_sec")
    
    # Define the cross-validation object
    cv = CrossValidator(estimator=gbt,
                        estimatorParamMaps=paramGrid,
                        evaluator=evaluator_rmse, 
                        numFolds=4)

    # Train the model
    cvModel = cv.fit(train_data)

    # Get the best model
    bestModel = cvModel.bestModel

    # Evaluate the best model on the test data
    gbt_predictions = bestModel.transform(test_data)
    gbt_rmse = evaluator_rmse.evaluate(gbt_predictions)
    gbt_r2 = evaluator_r2.evaluate(gbt_predictions)

    bestModel.save("models/GBT")
    return gbt_predictions, gbt_rmse, gbt_r2

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# run models
LR_PREDICTIONS, LR_RMSE, LR_R2 = run_lr(TEST_DATA, TRAIN_DATA)
RF_PREDICTIONS, RF_RMSE, RF_R2 = run_rf(TEST_DATA, TRAIN_DATA)
# gbt_predictions, gbt_rmse, gbt_r2 = run_gbt(test_data, train_data)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# print metrics

print "METRICS:"
print "Linear Regression:"
print "\t- RMSE:", LR_RMSE
print "\t- R2:", LR_R2
LR_PREDICTIONS.select("trip_time_sec", "prediction").show()

print "Random Forest:"
print "\t- RMSE:", RF_RMSE
print "\t- R2:", RF_R2
RF_PREDICTIONS.select("trip_time_sec", "prediction").show()

# print("Gradient Boosted Tree:")
# print("\t- RMSE:", gbt_rmse)
# print("\t- R2:", gbt_r2)
# gbt_predictions.select("trip_time_sec", "prediction").show()

CSV_DIR = 'output'

EVALUATION_CSV = ('metic,lr,rf,gbt\nrmse,%f,%f,%f\nr2,%f,%f,%f'
                  %(LR_RMSE, RF_RMSE, 0, LR_R2, RF_R2, 0))
with open("%s/evaluation.csv"%(CSV_DIR), "w") as file:
    file.write(EVALUATION_CSV)

LR_PREDICTIONS = LR_PREDICTIONS.select("trip_time_sec", "prediction")
LR_PREDICTIONS.select([F.col(c).cast(StringType()) for c in LR_PREDICTIONS.columns])
# columns: trip_time_sec,prediction
LR_PREDICTIONS.write.csv("%s/lr" % CSV_DIR)

RF_PREDICTIONS = RF_PREDICTIONS.select("trip_time_sec", "prediction")
RF_PREDICTIONS.select([F.col(c).cast(StringType()) for c in RF_PREDICTIONS.columns])
# columns: trip_time_sec,prediction
RF_PREDICTIONS.write.csv("%s/rf" % CSV_DIR)

# gbt_predictions = gbt_predictions.select("trip_time_sec", "prediction")
# gbt_predictions.select([F.col(c).cast(StringType()) for c in gbt_predictions.columns])
# # columns: trip_time_sec,prediction
# gbt_predictions.write.csv("%s/gbt" % csv_dir)
