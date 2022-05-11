import numpy as np
import yaml
import pandas as pd
import argparse
from sklearn.impute import KNNImputer
from src.utils.logger import App_Logger
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import SelectKBest

file_object=open("logs/Loggings.txt", 'a+')
logger_object=App_Logger()

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def preprocessing(config_path):
    """
    We need to preprocess the data. We need to impute the missing values. We have to handle the categorical data.
    Mutual Information gain technique for Feature Selection is used.
    """
    config = read_params(config_path)
    
    data_path = config["data_source"]["source"]

    df=pd.read_csv(data_path)

    ## Count/Frequency Encoding for Categorical Variables

    try:
        ## Counting the number of occurances of each category as dictionary
        order_status_dict = df["order_status"].value_counts()
        payment_type_dict = df["payment_type"].value_counts()
        product_category_name_english_dict = df["product_category_name_english"].value_counts()
        timing_dict = df["timing"].value_counts()
        Seasons_dict = df["Seasons"].value_counts()

        ## Above data is now saved in json format
        order_status_dict.to_json("encoded_files/order_status.json")
        payment_type_dict.to_json("encoded_files/payment_type.json")
        product_category_name_english_dict.to_json("encoded_files/product_category_name_english.json")
        timing_dict.to_json("encoded_files/timing.json")
        Seasons_dict.to_json("encoded_files/Seasons.json")

        ## Encoded data is getting mapped to the original dataframe
        df["order_status_encoded"] = df["order_status"].map(order_status_dict)
        df["payment_type_encoded"] = df["payment_type"].map(payment_type_dict)
        df["product_category_name_english_encoded"] = df["product_category_name_english"].map(product_category_name_english_dict)
        df["timing_encoded"] = df["timing"].map(timing_dict)
        df["Seasons_encoded"] = df["Seasons"].map(Seasons_dict)

        logger_object.log(file_object,'Count/Frequency Encoding for Categorical Variables Successful.')

    except Exception as e:
        logger_object.log(file_object, 'There was a problem while encoding the data.')
        logger_object.log(file_object,str(e))


    ## KNN Imputation for Missing Variables
    try:
        imputer = KNNImputer(n_neighbors=5, missing_values=np.nan)

        new_array = imputer.fit_transform(df)

        df = pd.DataFrame(data=new_array, columns= df.columns)

        logger_object.log(file_object, 'KNN Imputation Successful.')

    except Exception as e:
        logger_object.log(file_object, 'There was a problem while imputing the data.')
        logger_object.log(file_object,str(e))


    ## Selecting all the features may not be useful.
    ## We can use Mutual Information gain technique for Feature Selection.
    try:
        y = df["review_score"]
        x = df.drop(columns=["review_score"])

        x_train, x_test, y_train, y_test=train_test_split(x,y, test_size=0.15, random_state=111)

        mutual_info = mutual_info_classif(x_train, y_train)
        mutual_info = pd.Series(mutual_info)
        mutual_info.index = x_train.columns

        sel_cols = SelectKBest(mutual_info_classif, k=13)
        sel_cols.fit(x_train, y_train)
        col = list(x_train.columns[sel_cols.get_support()]) + ["review_score"]

        df = df[col]

        logger_object.log(file_object, 'The data has been preprocessed.')

    except Exception as e:
        logger_object.log(file_object, 'There was a problem while selecting the features.')
        logger_object.log(file_object,str(e))


    ## Saving the dataframe to a csv file.
    try:
        df.to_csv("data/preprocessed_data.csv")
        logger_object.log(file_object, 'The data has been preprocessed and saved to the file data/preprocessed_data.csv')

    except Exception as e:
        logger_object.log(file_object, 'There was a problem while saving the data.')
        logger_object.log(file_object,str(e))

if __name__ =="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data=preprocessing(config_path=parsed_args.config)