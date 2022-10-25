# mlflow-examples - xgboost

## Overview
* XBGoost with sklearn train and predict.
* Saves model in xgboost format.
* Wine quality dataset [train/wine-quality-white.csv](../../data/train/wine-quality-white.csv).

## Training

```
python train.py --experiment_name xgboost --estimators 20000 --max_depth 5 
```
```
mlflow run . --experiment_name xgboost -P estimators=20000 -P max_depth=5 
```

## Predictions

Score with mlflow.xgboost.load_model and mlflow.pyfunc.load_model.
You can either use a `runs` or `models` URI.
```
python predict.py runs:/7e674524514846799310c41f10d6b99d/xgboost-model
```

```
python predict.py models:/xgboost_wine/production
```

```

To Run XGB model
python XGBoost_demo.py --experiment_name xgboost --estimators 30000 --max_depth 10 --min_child_weight 2

To Run Elastic Net model
python ElasticNet_demo.py --experiment_name Elastic_net --alpha 1 --l1_ratio 1


```

## made changes for my demo today ar 6:42
