from flask import Flask, render_template, request, jsonify
import json
import os
from thabit.utils.logger import get_logger

app = Flask(__name__)
logger = get_logger()

# set the template folder to the root folder
app.template_folder = os.path.join(os.path.dirname(__file__), "..", "templates")
logger.info(f"Template folder: {app.template_folder}")


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
def dataset(dataset_path):
    return render_template("dataset.html")


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
    # check if the path exists
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
    # save the dataset file
    with open(dataset_path, "w") as f:
        json.dump(request.json, f)
    return jsonify({"status": "success"})
