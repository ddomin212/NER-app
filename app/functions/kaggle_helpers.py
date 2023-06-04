"""
This module contains helper functions for inference of the uploaded PDF file.
"""

import subprocess
import json
import os
import pandas as pd


def get_ner_kaggle(uploaded_file, first_time):
    """
    Runs a bash script to extract named entities from a PDF
    file uploaded to the app, with a spacy NER model inside a
    Kaggle Notebook for faster inference. The extracted entities
    are returned as a list of lists, where each inner list represents
    a row in the output Excel file.

    Args:
        uploaded_file (FileStorage): The uploaded PDF file.
        first_time (str): A string indicating whether this is the first time the
                                script is being run. Necessary for the Kaggle API.

    Returns:
        List[List[str]]: A list of lists representing the rows in the output Excel file.
    """
    uploaded_file.save("app/static/generated/dataset/file.pdf")
    # run the bash script
    subprocess.run(["bash", "app/functions/kaggle.sh", first_time], check=True)
    # continue with Python code
    print("The script has finished executing.")
    return pd.read_excel("app/static/generated/output/data.xlsx").values.tolist()


def init_kaggle():
    """
    Initializes a Kaggle notebook for the given user email.

    Args:
        user_email (str): The email of the user to initialize the notebook for.
    """
    init_dataset()
    init_kernel()
    os.mkdir("app/static/generated/output")


def init_dataset():
    """
    Initializes a Kaggle dataset.

    Args:
        None
    """
    os.mkdir("app/static/generated/dataset")
    kaggle_metadata = {
        "title": "ner-app",
        "id": "dandominko/ner-app",
        "licenses": [{"name": "CC0-1.0"}],
    }
    json.dump(
        kaggle_metadata,
        open(
            "app/static/generated/dataset/dataset-metadata.json", "w", encoding="utf-8"
        ),
    )


def init_kernel():
    """
    Initializes a Kaggle kernel.

    Args:
        None
    """
    os.mkdir("app/static/generated/kernel")
    kaggle_metadata = {
        "id": "dandominko/ner-app-kernel",
        "title": "ner-app-kernel",
        "code_file": "ner.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": True,
        "keywords": ["gpu"],
        "dataset_sources": ["dandominko/ner-app"],
        "kernel_sources": [],
        "competition_sources": [],
    }
    subprocess.run(
        ["mv", "app/static/ner.ipynb", "app/static/generated/kernel/ner.ipynb"],
        check=True,
    )
    json.dump(
        kaggle_metadata,
        open("app/static/generated/kernel/kernel-metadata.json", "w", encoding="utf-8"),
    )
