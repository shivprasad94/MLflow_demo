import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sklearn.linear_model import ElasticNet
import sys
import warnings

print("MLflow Version:", mlflow.__version__)
print("MLflow Tracking URI:", mlflow.get_tracking_uri())
print("XGBoost version:",xgb.__version__)
client = mlflow.tracking.MlflowClient()

def build_data(data_path):
    data = pd.read_csv(data_path)
    train, test = train_test_split(data, test_size=0.30, random_state=2019)

    # The predicted column is "quality" which is a scalar from [3, 9]
    X_train = train.drop(["quality"], axis=1)
    X_test = test.drop(["quality"], axis=1)
    y_train = train["quality"]
    y_test = test["quality"]

    return X_train, X_test, y_train, y_test 

def train(data_path, model_name,alpha,l1_ratio):
    X_train, X_test, y_train, y_test = build_data(data_path)
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        experiment_id = run.info.experiment_id
        print("MLflow:")
        print("  run_id:", run_id)
        print("  experiment_id:", experiment_id)
        print("  experiment_name:", client.get_experiment(experiment_id).name)


        # Create and fit model
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        model.fit(X_train, y_train)

        # MLflow metrics
        predictions = model.predict(X_test)
        print("predictions:",predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        # MLflow params
        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        # Log model
        mlflow.sklearn.log_model(model, "ElasticNet", registered_model_name=model_name)


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--experiment_name", dest="experiment_name", help="Experiment name", default=None)
    parser.add_argument("--model_name", dest="model_name", help="Registered model name", default=None)
    parser.add_argument("--data_path", dest="data_path", help="Data path", default="data/train/wine-quality-white.csv")
    parser.add_argument("--alpha", dest="alpha", help="alpha", default=0.5, type=float)
    parser.add_argument("--l1_ratio", dest="l1_ratio", help="l1_ratio", default=0.5, type=float)
    parser.add_argument("--min_child_weight", dest="min_child_weight", help="Min child weight", default=1.5, type=float)
    args = parser.parse_args()
    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")
    if args.experiment_name:
        mlflow.set_experiment(args.experiment_name)
    model_name = None if not args.model_name or args.model_name == "None" else args.model_name
    train(args.data_path, model_name,args.alpha,args.l1_ratio)
