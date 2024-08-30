from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import CountVectorizer, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from config import Config

def create_spark_session():
    return SparkSession.builder \
        .appName("ModelTraining") \
        .config("spark.mongodb.input.uri", f"{Config.MONGODB_URI}/{Config.DATABASE_NAME}.{Config.PROCESSED_NEWS_COLLECTION}") \
        .config("spark.mongodb.output.uri", f"{Config.MONGODB_URI}/{Config.DATABASE_NAME}.trained_model") \
        .getOrCreate()

def load_data(spark):
    return spark.read \
        .format("com.mongodb.spark.sql.DefaultSource") \
        .load()

def prepare_data(df):
    return df.randomSplit([0.8, 0.2], seed=42)

def create_feature_pipeline():
    return Pipeline(stages=[
        CountVectorizer(inputCol="content", outputCol="rawFeatures"),
        IDF(inputCol="rawFeatures", outputCol="features")
    ])

def create_model():
    return LogisticRegression(featuresCol="features", labelCol="label", maxIter=10)

def create_param_grid(model):
    return ParamGridBuilder() \
        .addGrid(model.regParam, [0.1, 0.01, 0.001]) \
        .addGrid(model.elasticNetParam, [0.0, 0.5, 1.0]) \
        .build()

def create_cross_validator(model, param_grid):
    evaluator = BinaryClassificationEvaluator(labelCol="label")
    return CrossValidator(estimator=model,
                          estimatorParamMaps=param_grid,
                          evaluator=evaluator,
                          numFolds=5)

def train_model(training_data, cv):
    return cv.fit(training_data)

def evaluate_model(model, test_data):
    predictions = model.transform(test_data)
    accuracy = predictions.filter(predictions.label == predictions.prediction).count() / test_data.count()
    return accuracy

def save_model(model):
    model_output_path = f"{Config.MONGODB_URI}/{Config.DATABASE_NAME}.trained_model"
    model.write().overwrite().save(model_output_path)

def main():
    spark = create_spark_session()
    
    try:
        # Load and prepare data
        news_articles_df = load_data(spark)
        training_data, test_data = prepare_data(news_articles_df)

        # Create and fit feature pipeline
        feature_pipeline = create_feature_pipeline()
        feature_model = feature_pipeline.fit(training_data)

        # Transform data
        training_data_transformed = feature_model.transform(training_data)
        test_data_transformed = feature_model.transform(test_data)

        # Create and train model
        lr = create_model()
        param_grid = create_param_grid(lr)
        cv = create_cross_validator(lr, param_grid)
        cv_model = train_model(training_data_transformed, cv)

        # Get best model
        best_model = cv_model.bestModel

        # Evaluate model
        accuracy = evaluate_model(best_model, test_data_transformed)
        print(f"Model accuracy: {accuracy}")

        # Save model
        save_model(best_model)

        print("Model training completed and saved to MongoDB.")

    finally:
        spark.stop()

if __name__ == "__main__":
    main()