from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
import yaml
from src.utils.logger import App_Logger
import yaml
import argparse
import csv

file_object=open("logs/Loggings.txt", 'a+')
logger_object=App_Logger()

class cassandra_operations:
    """
    This class is created to make the connection with the database. And it is used to
    download the data from the database.
    """
    def __init__(self):
        
        with open("params.yaml", 'r') as stream:
            try:
                params = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        credential = params['cassandra_database']
        
        self.CLIENT_ID = credential['CLIENT_ID']
        self.CLIENT_SECRET = credential['CLIENT_SECRET']
        self.table_name = credential['table_name']
        self.keyspace = credential['keyspace']


    def db_connection(self):
        """
        This function is used to connect to the database. We need a secure connect zip file to connect to the
        database. Also, we will be needing the CLIENT_ID and CLIENT_SECRET to connect to the database.
        Finally, we will be using the keyspace to connect to the database.
        """
        try:
            cloud_config = {
                'secure_connect_bundle': 'src/utils/secure-connect-olistproject.zip'
            }
            auth_provider = PlainTextAuthProvider(self.CLIENT_ID, self.CLIENT_SECRET)
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session =cluster.connect()
            logger_object.log(file_object, 'Connection Established.')
        except Exception as e:
            logger_object.log(file_object, 'There was a connection problem.')
            logger_object.log(file_object,str(e))

        return session


    def download_table(self, filename):
        """
        Olist data is stored in cassandra database. This function is used to download the data from the database.
        """
        session = self.db_connection()

        try:
            ## Downloading the data from the database.
            rows=session.execute("SELECT * FROM {}.{}".format(self.keyspace, self.table_name))

            data=[]
            for i in rows:
                data.append(i)

            ## Converting the data into csv format and saving it.
            pd.DataFrame(data).to_csv("data_ingestion/{}.csv".format(filename))
            logger_object.log(file_object, f"All the Data has been downloaded from the table {self.table_name}")
        except Exception as e:
            logger_object.log(file_object, 'There was a problem while downloading the data from the Table.')
            logger_object.log(file_object,str(e))

        else:
            logger_object.log(file_object,'All the Data has been downloaded from the table {} successfully.'.format(self.table_name))
        finally:
            session.shutdown()
            logger_object.log(file_object, 'Connection closed...')


    if __name__=="__main__":
        args = argparse.ArgumentParser()
        args.add_argument("--config", default="params.yaml")
        parsed_args = args.parse_args()
        data=download_table(config_path=parsed_args.config)