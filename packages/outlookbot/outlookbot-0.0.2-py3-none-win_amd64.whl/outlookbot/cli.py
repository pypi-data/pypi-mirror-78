'''
File: cli.py
Created: 2020-08-27
Author: Subhendu R Mishra 
'''

import click

from .config import Config
from .outlook_client import send_email, read_email
from .setup_utils import do_setup


@click.group()
def cli():
    """ Outlook-bot 

    Automate Outlook tasks. 
        - Send emails 
        - Read emails    

    Author : Subhendu  (https://github.com/subhrm/email-automation)
    """
    pass


@click.command()
@click.option("--config-file", "-c", help="Config File")
@click.option("--email-data-file", "-d", help="Email data File")
@click.option("--template-file", "-t", help="The template file")
# @click.option("--format", "-f", type=click.Choice(['text', 'html'], case_sensitive=False), 
#               default="text", show_default=True, 
#               help="Email Format")
@click.option("--dry-run", "-d", is_flag=True, default=False, show_default=True, 
              help="Dry run")
def fire(config_file, email_data_file, template_file, dry_run):
    """
        Send email
    """
    config = Config(config_file)

    if not email_data_file:
        email_data_file = config.EMAIL_DATA_FILE

    if not template_file:
        template_file = config.TEMPLATE_FILE

    send_email(email_data_file, template_file, dry_run)


@click.command()
@click.option("--data-file-type", "-t", type=click.Choice(['csv', 'xlsx'], case_sensitive=False), default="xlsx", 
              show_default=True, help="Email Data file type")
def setup(data_file_type):
    """ Setup the program
    """
    data_file_name = f"outlookbot-data-template.{data_file_type}"
    template_file_name = "outlookbot-email-template.txt"
    config_file_name = "config.json"

    do_setup(data_file_name=data_file_name, 
             template_file_name=template_file_name,
             config_file_name=config_file_name)


@click.command()
@click.option("--folder-name", "-fn", default="inbox", show_default=True, 
              help="Outlook Email folder name")
@click.option("--output-file", "-o", default="emails.xlsx", show_default=True, 
              help="The file where data would be saved")
def read(folder_name, output_file):
    """Read email
    """
    read_email(folder_name, output_file)


cli.add_command(fire)
cli.add_command(read)
cli.add_command(setup)
