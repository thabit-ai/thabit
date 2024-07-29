from flask import Flask, render_template, request, jsonify
import json
import os
from thabit.utils.logger import get_logger
from thabit.constants.platform import DATASET_FOLDER
from glob import glob

app = Flask(__name__)
# logger = get_logger(function_name="ui.py")

# set the template folder to the root folder
app.template_folder = os.path.join(os.path.dirname(__file__), "..", "templates")
# logger.info(f"Template folder: {app.template_folder}")


@app.route("/config", methods=["GET"])
def config():
    config_path = request.args.get("config_path")
    # check if the file exists
    if not os.path.exists(config_path):
        config_data = {}
    else:
        # load the config file
        with open(config_path, "r") as f:
            config_data = json.load(f)
    return render_template("config.html", config_data=config_data)


@app.route("/dataset", methods=["GET"])
def dataset():
    dataset_path = request.args.get("dataset")
    version = request.args.get("version")
    full_dataset_path = os.path.join(DATASET_FOLDER, dataset_path)
    if not version:
        version = 1
    # check if the file exists
    if not os.path.exists(full_dataset_path):
        dataset = {}
        # create the folder
        os.makedirs(full_dataset_path)
    else:
        # get the dataset latest version
        # check if the folder has any .json files
        if glob(full_dataset_path + "/*.json"):
            latest_version = max(
                [
                    int(f.split(".")[0])
                    for f in os.listdir(full_dataset_path)
                    if f.endswith(".json")
                ]
            )
        else:
            latest_version = 0

        if latest_version > 0:
            with open(
                full_dataset_path + f"/{latest_version}.json",
                "r",
            ) as f:
                dataset = json.load(f)
        else:
            dataset = {}
    return render_template("dataset.html", dataset=dataset)


@app.route("/save_config", methods=["POST"])
def save_config(config_path):
    # check if the path exists
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    # save the config file
    with open(config_path, "w") as f:
        json.dump(request.json, f)
    return jsonify({"status": "success"})


@app.route("/save_dataset", methods=["POST"])
def save_dataset(dataset_path):
    logger = get_logger(function_name="save_dataset")
    full_dataset_path = os.path.join(DATASET_FOLDER, dataset_path)
    # the files in the folder are named as 1.json, 2.json, 3.json etc. referring to the version.
    # check the latest version and add a new one
    try:
        latest_version = max(
            [
                int(f.split(".")[0])
                for f in os.listdir(full_dataset_path)
                if f.endswith(".json")
            ]
        )
        if latest_version == "":
            latest_version = 0
        new_version = latest_version + 1
    except Exception as e:
        logger.error(f"Error getting latest version: {e}")
        return jsonify({"status": "error", "message": "Error getting latest version"})
    # save the dataset file
    try:
        with open(full_dataset_path + f"/{new_version}.json", "w") as f:
            json.dump(request.json, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving dataset: {e}")
        return jsonify({"status": "error", "message": "Error saving dataset"})
    return jsonify({"status": "success"})
