import os
import yaml
import argparse
import pandas as pd
from sklearn.utils import resample
from src.utils.logger import App_Logger

file_object=open("logs/Loggings.txt", 'a+')
logger_object=App_Logger()

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def balance(config_path):
    """
    The data is imbalance. This is because most of the people have rated the 5 score in their reviews.
    Since the data is imbalanced, we need to balance the data. We are going to use the resampling technique.
    """
    config = read_params(config_path)
    data_path = config["data_source"]["preprocessed"]

    # Read the data
    df = pd.read_csv(data_path)
 
    try: 
        df1 = df[(df['review_score']==1)]
        df2 = df[(df['review_score']==2)]
        df3 = df[(df['review_score']==3)]
        df4 = df[(df['review_score']==4)]
        df5 = df[(df['review_score']==5)]

        # upsample minority classes
        df1_sampled = resample(df1, replace=True, n_samples= 55899, random_state=42)
        df2_sampled = resample(df2, replace=True, n_samples= 55899, random_state=42)
        df3_sampled = resample(df3, replace=True, n_samples= 55899, random_state=42)
        df4_sampled = resample(df4, replace=True, n_samples= 55899, random_state=42)  

        # Combine majority class with upsampled minority class
        df = pd.concat([df1_sampled, df2_sampled, df3_sampled, df4_sampled, df5])

        logger_object.log(file_object,'Data Balance Successful.')
 
    except Exception as e:
        logger_object.log(file_object,'Data Balance Failed.')
        logger_object.log(file_object,str(e))


    ## After re-sampling, all the data have been converted to float type. For this usecase, we can convert it back to int type.
    try:
        lst_col = list(df.columns)
        for col in lst_col:
            df = df.astype({col: int}, errors='raise')
        logger_object.log(file_object,'Data Type Conversion Successful.')

    except Exception as e:
        logger_object.log(file_object,'Data Type Conversion Failed.')
        logger_object.log(file_object,str(e))

    
    ## Write the dataframe to csv file
    try:
        df.to_csv(config["data_source"]["final"], index=False)
        logger_object.log(file_object,'Data Write Successful.')

    except Exception as e:
        logger_object.log(file_object,'Data Write Failed.')
        logger_object.log(file_object,str(e))

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data=balance(config_path=parsed_args.config)