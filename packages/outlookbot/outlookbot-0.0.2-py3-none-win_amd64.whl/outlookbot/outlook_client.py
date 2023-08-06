'''
File: outlook_client.py
Created: 2020-08-28
Author: Subhendu R Mishra 
'''
import os
import win32com.client as win32
import pandas as pd
from tqdm import tqdm

from .email_template import EmailTemplate
from .data_file_utils import read_data_file, match_with_template


def send_email(email_data_file, template, dry_run=False):

    if not os.path.exists(template):
        raise FileNotFoundError(f"Template file {template} not found")

    with open(template) as tin:
        et = EmailTemplate(tin.read())

    data_df = read_data_file(email_data_file)
    data_df.fillna("", inplace=True)

    match_with_template(data_df, et)

    # Open up an outlook email
    outlook = win32.gencache.EnsureDispatch('Outlook.Application')

    for row in tqdm(data_df.itertuples()):
        new_mail = outlook.CreateItem(0)

        # Label the subject
        new_mail.Subject = et.get_subject(row._asdict())
        new_mail.Body = et.get_body(row._asdict())

        # Add the to and cc list
        new_mail.To = row.TO
        if row.CC:
            new_mail.CC = row.CC
        if row.BCC:
            new_mail.BCC = row.BCC 

        if row.ATTACHMENTS:
            attachments = row.ATTACHMENTS.split("|")

            for fname in attachments:
                if os.path.exists(fname):
                    new_mail.Attachments.Add(Source=str(fname))
                else:
                    tqdm.write(f"File {fname} doesn't exist. Skipping it")

        if dry_run:
            # Display the email
            new_mail.Display(True)
        else:
            new_mail.Send()


def get_outlook_folder(folder_name=""):
    outlook = win32.gencache.EnsureDispatch('Outlook.Application').GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)

    if folder_name.lower() == "inbox":

        return inbox

    folders = inbox.Folders
    for i in range(1, folders.Count + 1):
        folder = folders.Item(i)
        fname = folder.Name
        if fname.lower() == folder_name.lower():
            return folder

    raise FileNotFoundError(f"{folder_name} not found")


def read_email(folder_name, output_file):
    """Read Emails from a folder in outlook using MAPI Interface
    Args:
        folder_name (str, optional): [Folder Name]. Defaults to "".
    """

    if os.path.exists(output_file):
        raise FileExistsError(f"The file {output_file} exists")

    ext = os.path.splitext(output_file)[-1].lower()
    if ext not in (".csv", ".xlsx"):
        raise NotImplementedError(f"{ext} file not supported. Only CSV and Excel files supported")

    mailbox = get_outlook_folder(folder_name)

    count = mailbox.Items.Count
    mails = []
    print(f"Reading {count} emails from {folder_name} folder")
    for i in tqdm(range(1, count + 1)):
        mail = mailbox.Items.Item(i)
        mail_obj = {
            "SenderName": mail.SenderName,
            "SenderEmailAddress": mail.SenderEmailAddress,
            "Subject": mail.Subject,
            "To": mail.To,
            "CC": mail.CC,
            "Body": mail.Body,
            "ReceivedTime": str(mail.ReceivedTime),
        }
        mails.append((mail_obj))

    df = pd.DataFrame(mails)

    if ext == ".xlsx":
        df.to_excel(output_file, index=False)
    elif ext == ".csv":
        df.to_csv(output_file, index=False)
