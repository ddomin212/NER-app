import subprocess
import json
import os
import pandas as pd
import subprocess


def get_ner_kaggle(uploaded_file, first_time):
    uploaded_file.save("app/static/generated/dataset/file.pdf")
    # run the bash script
    subprocess.run(["bash", "app/functions/kaggle.sh", first_time])
    # continue with Python code
    print("The script has finished executing.")
    return pd.read_excel("app/static/generated/output/data.xlsx").values.tolist()


def init_kaggle():
    init_dataset()
    init_kernel()
    os.mkdir("app/static/generated/output")


def init_dataset():
    os.mkdir("app/static/generated/dataset")
    kaggle_metadata = {
        "title": "ner-app",
        "id": "dandominko/ner-app",
        "licenses": [{"name": "CC0-1.0"}],
    }
    json.dump(
        kaggle_metadata, open("app/static/generated/dataset/dataset-metadata.json", "w")
    )


def init_kernel():
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
        ["mv", "app/static/ner.ipynb", "app/static/generated/kernel/ner.ipynb"]
    )
    json.dump(
        kaggle_metadata, open("app/static/generated/kernel/kernel-metadata.json", "w")
    )
