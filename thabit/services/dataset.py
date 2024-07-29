import os
from glob import glob
from thabit.utils.logger import get_logger
from thabit.constants.platform import DATASET_FOLDER
import json

DATASET_FOLDER = "datasets"
logger = get_logger()


def read_dataset(name):
    # read dataset from dataset folder
    logger.info(f"Reading dataset {name}")
    dataset_path = os.path.join(DATASET_FOLDER, name)
    logger.info(f"Dataset path: {dataset_path}")
    if not os.path.exists(dataset_path):
        return None
    # check if the folder has .json files
    if not glob(os.path.join(dataset_path, "*.json")):
        logger.error(f"Dataset {name} does not have any .json files")
        return None
    # read the max version json file
    latest_version = max(
        [int(f.split(".")[0]) for f in os.listdir(dataset_path) if f.endswith(".json")]
    )
    logger.info(f"Latest version: {latest_version}")
    dataset_file = os.path.join(dataset_path, f"{latest_version}.json")
    logger.info(f"Dataset file: {dataset_file}")
    with open(dataset_file, "r") as f:
        return json.load(f)
