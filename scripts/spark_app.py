import sys
import os
import psutil
import time
import numpy as np
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler, MinMaxScaler
from pyspark.ml import Pipeline
from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType
from lightgbm.spark import LightGBMClassifier
from sklearn.metrics import classification_report

OPTIMIZED = True if sys.argv[1] == "True" else False
time_start = time.time()

SparkContext.getOrCreate(SparkConf().setMaster('spark://spark-master:7077')).setLogLevel("INFO")
spark = SparkSession.builder.master("spark://spark-master:7077").appName("diabetes_prediction").getOrCreate()

data = spark.read.format("csv").option("header", "true").option('inferSchema', 'true').load("hdfs://namenode:9000/data/diabetes_012_health_indicators.csv")

data = data.drop("Education", "Income")

if OPTIMIZED:
    data.cache()
    data = data.repartition(4)

binary_cols = ['HighBP', 'HighChol', 'CholCheck', 'Smoker', 'Stroke', 
               'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
               'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'DiffWalk', 'Sex']
               
numeric_cols = ['BMI', 'MentHlth', 'PhysHlth']
ordinal_cols = ['GenHlth', 'Age']
target_col = 'Diabetes_012'

for column in data.columns:
    data = data.withColumn(column, col(column).cast(DoubleType()))

train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)

if OPTIMIZED:
    train_data = train_data.repartition(4)
    test_data = test_data.repartition(4)
    train_data.cache()
    test_data.cache()

assemblers = []

numeric_assembler = VectorAssembler(inputCols=numeric_cols, outputCol="numeric_features")
numeric_scaler = StandardScaler(inputCol="numeric_features", outputCol="scaled_numeric", 
                               withStd=True, withMean=True)
assemblers.extend([numeric_assembler, numeric_scaler])

ordinal_assembler = VectorAssembler(inputCols=ordinal_cols, outputCol="ordinal_features")
ordinal_scaler = MinMaxScaler(inputCol="ordinal_features", outputCol="scaled_ordinal",
                             min=0, max=1)
assemblers.extend([ordinal_assembler, ordinal_scaler])

final_assembler = VectorAssembler(
    inputCols=binary_cols + ["scaled_numeric", "scaled_ordinal"],
    outputCol="features"
)

lgbm = LightGBMClassifier(
    featuresCol="features",
    labelCol=target_col,
    objective="multiclass",
    seed=42
)

pipeline = Pipeline(stages=assemblers + [final_assembler, lgbm])

model = pipeline.fit(train_data)

predictions = model.transform(test_data)

pred_pandas = predictions.select(target_col, "prediction").toPandas()
y_true = pred_pandas[target_col].values
y_pred = pred_pandas["prediction"].values

diabetes_labels = ["No diabetes (0)", "Prediabetes (1)", "Diabetes (2)"]
print(classification_report(y_true, y_pred, target_names=diabetes_labels, zero_division=0))

time_res = time.time() - time_start
RAM_res = psutil.Process(os.getpid()).memory_info().rss / (float(1024)**2)
spark.stop()

with open('/log.txt', 'a') as f:
    f.write("Time: " + str(time_res) + " seconds, RAM: " + str(RAM_res) + " Mb.\n")