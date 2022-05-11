import yaml
import pandas as pd
import argparse
from src.utils.logger import App_Logger
from src.utils.cassandra_operations import cassandra_operations

file_object=open("logs/Loggings.txt", 'a+')
logger_object=App_Logger()

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def get_data(config_path):
    """
    Olist data is stored in cassandra database. This function is used to download the data from the database.
    """
    config = read_params(config_path)
    cassandra_object = cassandra_operations()
    try:
        cassandra_object.download_table(config['cassandra_database']['table_name'])
        logger_object.log(file_object, 'All the Data has been downloaded from the table {}'.format(config['cassandra_database']['table_name']))
    except Exception as e:
        logger_object.log(file_object, 'There was a problem while downloading the data from the Table.')
        logger_object.log(file_object,str(e))

    

if __name__ =="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data=get_data(config_path=parsed_args.config)