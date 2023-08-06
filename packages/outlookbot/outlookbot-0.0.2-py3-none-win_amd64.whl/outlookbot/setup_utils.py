'''
File: utils.py
Created: 2020-08-31
Author: Subhendu R Mishra 
'''

import os
import json
import pandas as pd


mandatory_cols = [
    "TO",
    "CC",
    "BCC",
    "ATTACHMENTS"]


def do_setup(data_file_name, template_file_name, config_file_name):
    default_locs = [".", os.path.join(os.path.expanduser("~"), "outlookbot")]
    if not os.path.exists(default_locs[1]):
        os.makedirs(default_locs[1], exist_ok=True)

    for loc in default_locs:
        data_file_path = os.path.join(loc, data_file_name)
        generate_data_template(data_file_path)
        template_file_path = os.path.join(loc, template_file_name)
        generate_email_template(template_file_path)
        config_file_path = os.path.join(loc, config_file_name)
        generate_config_file(data_file_path, template_file_path, config_file_path)


def generate_data_template(file_name: str):

    ext = os.path.splitext(file_name)[-1].lower()
    if ext not in (".csv", ".xlsx"):
        raise NotImplementedError(f"{ext} file not supported. Only CSV and Excel files supported")

    if os.path.exists(file_name):
        print(f"File {file_name} already exists")
        return

    columns = mandatory_cols + [
        "CustomField1",
        "CustomField12",
        "CustomField3"
    ]
    df = pd.DataFrame(data=[[""] * len(columns)], columns=columns)

    if ext == ".csv":
        df.to_csv(file_name, index=False)

    elif ext == ".xlsx":
        df.to_excel(file_name, index=False)


def generate_email_template(file_name: str):

    if os.path.exists(file_name):
        print(f"File {file_name} already exists")
        return

    data = ["The subject is {{{{CustomField1}}}}", 
            "Hello {{CustomField2}},", 
            "This is about {{CustomField3}}",
            "Regards"]

    with open(file_name, "w") as fout:
        fout.write("\n".join(data))


def generate_config_file(data_file_path, template_file_path, config_file_path):
    config = {
        "TEMPLATE_FILE": template_file_path,
        "EMAIL_DATA_FILE": data_file_path,
    }

    if os.path.exists(config_file_path):
        print(f"File {config_file_path} already exists")
        return

    with open(config_file_path, "w") as fout:
        json.dump(config, fout, indent=4)
