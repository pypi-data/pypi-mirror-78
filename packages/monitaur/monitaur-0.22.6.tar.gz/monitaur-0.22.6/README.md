# Monitaur Client Library

Tested with the following versions of Python:

1. 3.8.5
1. 3.7.9
1. 3.6.12

## Install

```sh
$ pip install monitaur
```

## Methods

1. `add_model`: Adds metadata about the machine learning model to the system.
1. `record_training_tabular`: Sends trained model, prediction file, and optional anchors data to S3.
1. `record_training_image`: Sends trained image model to S3.
1. `record_transaction`: Sends transaction details to the API.
1. `read_transactions`: Retrieves transactions.
1. `add_metrics`: Add metric.

## Client Library Examples

```python
from monitaur import Monitaur


# create monitaur instance
monitaur = Monitaur(
    client_secret="changme",
    base_url="http://localhost:8008",
)

# train model
dataset = loadtxt("./_example/data.csv", delimiter=",")
seed = 7
test_size = 0.1
model_data = train_model(dataset, seed, test_size)
trained_model = model_data["trained_model"]
x_train = model_data["x_train"]
y_train = model_data["y_train"]
dump(trained_model, open(f"./_example/data.joblib", "wb"))


# add model to api
model_data = {
    "name": "Diabetes Classifier",
    "model_type": "xgboost",
    "model_class": "tabular",
    "library": "xgboost",
    "feature_number": 8,
    "owner": "Anthony Habayeb",
    "developer": "Andrew Clark",
    "influences": "anchors",
    # "counterfactual": True,
    "classification": True,
}
model_set_id = monitaur.add_model(**model_data)

# record training
record_training_data = {
    "model_set_id": model_set_id,
    "trained_model": Path("_example").joinpath("data", "data.joblib"),
    "training_data": x_train,
    "training_outcomes": y_train,
    "feature_names": [
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeF",
        "Age",
    ],
    category_map={"Age": [1, 5, 10]},
    # "re_train": True,
    # "processing": [
    #     Path(MODEL_DIR).joinpath("insurance.joblib"),
    #     Path(MODEL_DIR).joinpath("lightgbm_classifer.pickle"),
    #     Path(MODEL_DIR).joinpath("lightgbm_classifer.pkl"),
    #     Path(MODEL_DIR).joinpath("preprocessor.pkl"),
    #     Path(MODEL_DIR).joinpath("preprocessor.pickle"),
    # ],
}
monitaur.record_training_tabular(**record_training_data)

# record_training_data = {
#     "model_set_id": model_set_id,
#     "trained_model": trained_image_model,
#     # "re_train": True
# }
# monitaur.record_training_image(**record_training_data)

# record transaction
prediction = get_prediction([2, 84, 68, 27, 0, 26.7, 0.341, 32])
transaction_data = {
    "model_set_id": model_set_id,
    "trained_model": Path("_example").joinpath("data", "data.joblib"),
    "prediction_file": Path("_example").joinpath("prediction.py"),
    "prediction": prediction,
    "image": "cat.jpeg",  # required if 'model_class' is  'image'
    "python_version": "3.8.5",
    "ml_library_version": "0.90.0",
    "features": {
        "Pregnancies": 2,
        "Glucose": 84,
        "BloodPressure": 68,
        "SkinThickness": 27,
        "Insulin": 0,
        "BMI": 26.7,
        "DiabetesPedigreeF": 0.341,
        "Age": 32,
    },
    # "processing": [
    #     Path(MODEL_DIR).joinpath("insurance.joblib"),
    #     Path(MODEL_DIR).joinpath("lightgbm_classifer.pickle"),
    #     Path(MODEL_DIR).joinpath("lightgbm_classifer.pkl"),
    #     Path(MODEL_DIR).joinpath("preprocessor.pkl"),
    #     Path(MODEL_DIR).joinpath("preprocessor.pickle"),
    # ],
}
response = monitaur.record_transaction(**transaction_data)
print(response)

# read transactions by passing model_id and/or model_set_id
# both are optional arguments
transactions = monitaur.read_transactions(model_set_id=model_set_id)
print(transactions)

# add metric
metric_data = {
    "model_set_id": model_set_id,
    "feature_drift_enabled": True,
    "feature_drift": {"age": [9.0, 10.0, 11.0]},
    "model_drift_enabled": True,
    "model_drift": {"age": [9.0, 10.0, 11.0]},
    "bias_enabled": True,
    "bias_features_list": ["age"],
    "frequency": 10,
    "sample_size": 50,
}
metric = monitaur.add_metrics(**metric_data)
print(metric)
```

## API Examples

[requests](https://requests.readthedocs.io/):

```python
import requests

API_ENDPOINT = "http://localhost:8000"
CLIENT_SECRET = "eaa74a3d715a36ed6d40af3fb9f5916d8205cf2c"
MODEL_SET_ID = "b7f60d02-06c9-418c-943e-cf74fe61d613"

# get access and refresh tokens
tokens = requests.post(
    f"{API_ENDPOINT}/api/auth/?grant_type=client_credentials",
    data={"client_secret": CLIENT_SECRET}
)
access_token = tokens.json()["access"]
refresh_token = tokens.json()["refresh"]

headers = {"Authorization": f"Token {access_token}"}

# get model metadata
model = requests.get(f"{API_ENDPOINT}/api/models/set/{MODEL_SET_ID}", headers=headers)
print(model.json())
model_id = model.json()["id"]

# get transactions
transactions = requests.get(f"{API_ENDPOINT}/api/transactions/?model={model_id}", headers=headers)
for transaction in transactions.json():
    print(f"\n{transaction}")
```

cURL:

```sh
$ curl -X POST http://localhost:8000/api/auth/\?grant_type=client_credentials \
    -d '{"client_secret": "eaa74a3d715a36ed6d40af3fb9f5916d8205cf2c"}' \
    -H 'Content-Type: application/json'

$ curl -X GET "http://localhost:8000/api/models/set/b7f60d02-06c9-418c-943e-cf74fe61d613/" \
    -H "Authorization: Token 54321"
```

[httpie](https://httpie.org/):

```sh
$ http --json POST http://localhost:8000/api/auth/\?grant_type=client_credentials \
    client_secret=eaa74a3d715a36ed6d40af3fb9f5916d8205cf2c

$ http GET http://localhost:8000/api/models/set/b7f60d02-06c9-418c-943e-cf74fe61d613/ Authorization:"Token 54321"
```
