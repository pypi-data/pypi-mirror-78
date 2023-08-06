import base64
import json
import pickle
from datetime import datetime
from pathlib import Path, PurePath

import boto3
import dill
import joblib
import numpy as np
from mdutils.mdutils import MdUtils
from sklearn.preprocessing import LabelEncoder

from monitaur.virgil.alibi.tabular import AnchorTabular

from monitaur.exceptions import (  # noqa isort:skip
    ClientValidationError,
    CustomInfluencesError,
    FileError,
    MetricsError,
)


def get_influences(model_set_id, version, features, aws_credentials):
    """
    Downloads trained model and respective influences from s3.
    Then calculates influences based on the features

    Args:
        model_set_id: A UUID string for the monitaur model set.
        version: Monitaur model version.
        features: key/value pairs of the feature names and values.
        aws_credentials: dict of aws credentials

    Returns:
        dict of influences
    """

    influence_threshold = 0.95

    client = boto3.client(
        "s3",
        aws_access_key_id=aws_credentials["aws_access_key"],
        aws_secret_access_key=aws_credentials["aws_secret_key"],
        region_name=aws_credentials["aws_region"],
    )

    anchors_filename = f"{model_set_id}.anchors"
    s3_object = f"{model_set_id}/{version}/{anchors_filename}"

    with open(anchors_filename, "wb") as f:
        client.download_fileobj(aws_credentials["aws_bucket_name"], s3_object, f)

    with open(anchors_filename, "rb") as f:
        explainer = dill.load(f)
        # determine influences for transaction
        inputs = list(features.values())
        reshaped_inputs = np.asarray(inputs).reshape(1, len(inputs))
        influences = explainer.explain(reshaped_inputs, threshold=influence_threshold)

    if Path(anchors_filename).exists():
        Path(anchors_filename).unlink()

    return influences["names"]


def valid_model(extension, model_class):
    """
    Validates a trained model based on the model_class.

    Args:
        extension: File extension for the serialized model (.joblib, .pickle, '.tar', '.h5).
        model_class: 'tabular' or 'image'.

    Returns:
        True if valid
    """

    if model_class == "tabular" and extension not in [".joblib", ".pickle"]:
        raise FileError("Invalid model. Acceptable files: '.joblib', '.pickle'.")
    if model_class == "image" and extension not in [".joblib", ".tar", ".h5"]:
        raise FileError("Invalid model. Acceptable files: '.joblib', '.tar', '.h5'.")

    return True


def generate_anchors(
    extension, trained_model, feature_names, training_data, model_set_id
) -> str:
    """
    Generate anchor file

    Args:
        extension: File extension for the serialized model (.joblib, .pickle).
        trained_model: Instantiated model (.joblib, .pickle).
        feature_names: Model inputs.
        training_data: Training data (x training).
        model_set_id: A UUID string for the monitaur model set received from the API.

    Returns:
        anchor file path (.anchors)
    """

    if extension == ".joblib":
        trained_model_file = joblib.load(trained_model)
    else:
        trained_model_file = pickle.load(trained_model)

    predict_fn = lambda x: trained_model_file.predict_proba(x)  # NOQA
    explainer = AnchorTabular(predict_fn, feature_names)
    explainer.fit(training_data)

    filename_anchors = f"{model_set_id}.anchors"

    with open(filename_anchors, "wb") as f:
        dill.dump(explainer, f)

    return filename_anchors


def add_image(image):
    image_path = Path(image)

    if not image_path.exists():
        raise ClientValidationError("Image File path not valid")

    # Check the file extension
    extension = image_path.suffix
    if extension not in (".png", ".jpg", ".jpeg"):
        raise ClientValidationError("Invalid Image provided")

    file_size = float(image_path.stat().st_size) / (1024.0 ** 2)
    if file_size > 1:
        raise ClientValidationError(
            "Image Size greater than One (1) Megabyte. Choose a file with a lesser size"
        )

    with open(image, "rb") as img:
        image_byte = (base64.b64encode(img.read())).decode("utf-8")

    return image_byte


def validate_influences(model_influences, model_class, custom_influences):
    if model_influences == "custom-dict":
        if not isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is custom-dict, custom_influences must be a dict"
            )
    if model_influences == "custom-image":
        if not isinstance(custom_influences, PurePath):
            raise CustomInfluencesError(
                "When model.influences is custom-image, custom_influences must be a file path"
            )
    if model_influences == "anchors":
        if custom_influences or isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is anchors, custom_influences must be None"
            )
    if model_influences == "grad-cam":
        if custom_influences or isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is grad-cam, custom_influences must be None"
            )
    if not model_influences:
        if custom_influences or isinstance(custom_influences, dict):
            raise CustomInfluencesError(
                "When model.influences is None, custom_influences must be None"
            )

    return True


def upload_file_to_s3(
    model_set_id, version, filepath, aws_credentials, filename=None
) -> bool:
    """
    Uploads file to s3

    Args:
        model_set_id: A UUID string for the monitaur model set received from the API.
        version: Monitaur model version.
        filepath: Instantiated model file path
        aws_credentials: dict of aws credentials
        filename: optional name for the s3 object

    Returns:
        bool
    """

    client = boto3.client(
        "s3",
        aws_access_key_id=aws_credentials["aws_access_key"],
        aws_secret_access_key=aws_credentials["aws_secret_key"],
        region_name=aws_credentials["aws_region"],
    )

    if filename:
        s3_filename = filename
    else:
        s3_filename = filepath

    with open(filepath, "rb") as f:
        client.upload_fileobj(
            f,
            aws_credentials["aws_bucket_name"],
            f"{model_set_id}/{version}/{s3_filename}",
        )

    if Path(filepath).exists():
        Path(filepath).unlink()

    return True


def upload_training_files(
    model_set_id, version, aws_credentials, filepath, filetype="whitepaper"
):
    client = boto3.client(
        "s3",
        aws_access_key_id=aws_credentials["aws_access_key"],
        aws_secret_access_key=aws_credentials["aws_secret_key"],
        region_name=aws_credentials["aws_region"],
    )

    if not Path(filepath).exists():
        return False

    file_extension = Path(filepath).suffix

    file_s3_url = f"{model_set_id}/{version}/{filetype}{file_extension}"

    with open(filepath, "rb") as f:
        client.upload_fileobj(
            f, aws_credentials["aws_bucket_name"], file_s3_url,
        )

    return file_s3_url


def record_training_file_save(
    model_set_id, version, aws_credentials, x_train, y_train, y_labels=None
):
    """
    Description:
    Function to save training data
    Parameters
    ----------
        model_set_id: A UUID string for the monitaur model set received from the API.
        version: Monitaur model version.
        aws_credentials: dict of aws credentials
        x_train: numpy array
        y_train: numpy array
        y_labels: list of the y labels
    """
    x_path = Path("x_train.csv")
    y_path = Path("y_train.csv")

    labels_path = Path("y_labels.csv")

    # save and upload x_train csv to s3
    np.savetxt(x_path, x_train, delimiter=",")
    upload_file_to_s3(model_set_id, version, x_path, aws_credentials)

    # save and upload y_train csv to s3
    np.savetxt(y_path, y_train, delimiter=",")
    upload_file_to_s3(model_set_id, version, y_path, aws_credentials)

    if y_labels is not None:
        # save and upload y_labels to s3
        if isinstance(y_labels, np.ndarray):
            np.savetxt(labels_path, y_labels, delimiter=",")
        else:
            np.savetxt(labels_path, np.array(y_labels), delimiter=",", fmt="%s")

        upload_file_to_s3(model_set_id, version, labels_path, aws_credentials)


def validate_drift_metrics(enabled, drift_dict, classification, drift_type):
    if drift_dict and not enabled:
        raise MetricsError(f"If {drift_type} drift is not enabled, dict must be empty")

    if enabled:
        if drift_dict is None:
            raise MetricsError("Model Drift is Required")

        if not classification and drift_type == "model":
            if len(drift_dict) > 1 or "regression" not in drift_dict:
                raise MetricsError(
                    f"If classification is false, then model drift dict must only contain"
                    f" a single key/value pair with the key name of 'regression'"
                )

        if type(drift_dict) is not dict:
            raise MetricsError(f"Invalid format for {drift_type} drift dict")

        for drift in drift_dict:
            if type(drift_dict[drift]) is not dict:
                raise MetricsError(f"Invalid format for {drift_type} drift dict")

            drift_value = drift_dict[drift].get("values", None)
            if not drift_value:
                raise MetricsError(f"Invalid format for {drift_type} drift dict")

            range_value = drift_dict[drift].get("range", False)
            drift_dict[drift]["range"] = range_value

    return drift_dict


def validate_bias_metrics(enabled, feature_list):
    if feature_list and not enabled:
        raise MetricsError(f"If bias is not enabled, feature list must be empty")

    if enabled:
        if feature_list is None:
            raise MetricsError("Feature List is Required")

    return feature_list


def category_map_generator(df, categorical_names):
    """
    Definition:
    Function for creating a category map from pandas dataframes
    """
    category_map = {}
    for i in categorical_names:
        le = LabelEncoder()
        df[i] = le.fit_transform(df[i])
        category_map[i.lower()] = list(le.classes_)

    return df, category_map


def get_run_info(run, verbose=False):
    """
    Creates a human readable interpretation of an MLFlow Run

    Args:
        run: [mlflow.entities.Run] the MLFlow Run you want to create a report of
        verbose [bool]: set to True to get a long form report on the run (default False)

    Returns:
        [str] a report of all data that is captured by MLFlow
    """
    run_data = run.data.to_dictionary()
    run_info = run.info
    run_id = run_info.run_uuid
    run_name = run_data["tags"].get("mlflow.runName", "...")
    metrics = run_data["metrics"]
    params = run_data["params"]
    start_time_short = datetime.fromtimestamp(run_info.start_time / 1000).strftime(
        "%b %d %Y"
    )
    start_time = datetime.fromtimestamp(run_info.start_time / 1000).strftime(
        "%b/%d/%Y, %H:%M:%S"
    )
    end_time = datetime.fromtimestamp(run_info.end_time / 1000).strftime(
        "%b/%d/%Y, %H:%M:%S"
    )

    if not bool(metrics) or metrics is None:
        metrics = "No metrics collected"
    version_json_text = run_data["tags"].get("mlflow.log-model.history")
    if version_json_text:
        flavors = json.loads(version_json_text[1:-1])["flavors"]
        model_type = flavors["python_function"]["loader_module"].split(".")[1]
        version = flavors[model_type][f"{model_type}_version"]
    else:
        version = None

    if verbose:
        output = []
        output.append(f"Run ID: {run_info.run_id}")
        output.append(f"Run Name: {run_name}")
        if version:
            output.append(f"{model_type} Version: {version}")
        output.append(f"Params: {params}")
        output.append(f"Metrics: {metrics}")
        output.append(
            f"Duration: {(run_info.end_time - run_info.start_time) / 1000} seconds"
        )
        output.append(f"Start Time: {start_time}")
        output.append(f"End Time: {end_time}")
        output.append(f"Artifact URI: {run_info.artifact_uri}")
        output.append(f"ML Flow User: {run_data['tags']['mlflow.user']}")
        return "\n".join(output)
    else:
        # concise run information
        return f"{run_id[:5]} on {start_time_short}"


def get_metrics_report(
    client, experiment, report_name="MLFlowResults", title="MLFlow Training Results"
):
    """
    Creates a markdown file representing all training and metric data captured by MLFlow

    Args:
        client: [mlflow.tracking.MlflowClient] the MLFlow Client used to track your experiment
        experiment: [mlflow.entities.Experiment]: experiment that you wish to generate a report for
        report_name: [str] desired name for the markdown file (default "MLFlowResults")
        title: [str] desired name for the MLFlow report (default "MLFlow Training Results")

    Returns:
        None

    Side effects:
        Writes out a report_name.md file in the local dir
    """

    md_file = MdUtils(file_name=report_name, title=title)

    all_mlflow_runs = client.search_runs(experiment.experiment_id)

    if len(all_mlflow_runs) > 0:
        latest_run = all_mlflow_runs[0]
        md_file.new_header(level=1, title="Latest Run")
        md_file.new_header(level=2, title=get_run_info(latest_run))
        md_file.insert_code(get_run_info(latest_run, True))

    if len(all_mlflow_runs) > 1:
        md_file.new_header(level=1, title="Previous Runs")
        for run in all_mlflow_runs[1:]:
            md_file.new_header(level=2, title=get_run_info(run))
            md_file.insert_code(get_run_info(run, True))

    md_file.new_table_of_contents(table_title="Runs", depth=2)
    md_file.create_md_file()
