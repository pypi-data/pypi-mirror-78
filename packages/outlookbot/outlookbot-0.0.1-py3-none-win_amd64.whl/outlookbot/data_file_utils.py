'''
File: data_file_utils.py
Created: 2020-09-01
Author: Subhendu R Mishra 
'''

import os
import pandas as pd
from .setup_utils import mandatory_cols
from .email_template import EmailTemplate


def read_data_file(email_data_file: str) -> pd.DataFrame:
    if not os.path.exists(email_data_file):
        raise FileNotFoundError(f"Data file {email_data_file} not found")

    ext = os.path.splitext(email_data_file)[-1].lower()
    if ext not in (".csv", ".xlsx"):
        raise NotImplementedError(f"{ext} file not supported. Only CSV and Excel files supported")

    if ext == ".xlsx":
        df = pd.read_excel(email_data_file)
    elif ext == ".csv":
        df = pd.read_csv(email_data_file)

    if len(df) == 0:
        raise Exception("Empty email data file")

    _cols = df.columns
    for col in mandatory_cols:
        if col not in _cols:
            raise Exception(f"The column {col} not present in email data file {email_data_file}")

    return df


def match_with_template(df: pd.DataFrame, template_obj: EmailTemplate) -> None:

    template_vars: set = template_obj.required_variables
    _cols = df.columns

    missing = template_vars.difference(set(_cols))

    if len(missing) > 0:
        raise Exception(f"These template fields not found in email data file : {missing}")
