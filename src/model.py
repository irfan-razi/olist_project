from copyreg import pickle
import yaml
import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import pickle
from src.utils.logger import App_Logger

file_object=open("logs/Loggings.txt", 'a+')
logger_object=App_Logger()

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def train_test(config_path):
    """
    All the data is read from the csv file and then split into train and test data.
    After this, the data is split into X and y. The X is the data and y is the target.
    The target is the column which is to be predicted. Random Forest Classifier is used to train the data.
    We are using classification report to get the accuracy of the model. Since, this data is imbalanced,
    accuracy should not be the only criteria for checking the best model. That is why we are looking for the
    F1 score and Recall also for better judgement.
    """
    # Read the params.yaml file
    ## Path for source file
    config = read_params(config_path)
    data_path = config["data_source"]["final"]

    ## Path for saving the metrics report
    report_path=config["metrics"]["report"]

    ## Test and Train split configuration
    test_size_input = config["split_data"]["test_size"]
    random_state_no = config["split_data"]["random_state"]

    ## Random Forest Classifier configuration
    n_estimate_input = config["model_params"]["n_estimators"]
    criterion = config["model_params"]["criterion"]
    class_weight = config["model_params"]["class_weight"]
    min_samples_split = config["model_params"]["min_samples_split"]
    max_features_input = config["model_params"]["max_features"]
    
    
    try:
        # Read the data    
        df =pd.read_csv(data_path)
        logger_object.log(file_object,'Data Load Successful')

        x=df.drop(columns=["review_score"])
        y=df['review_score']

        # Split the data into train and test
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size_input,
                                                                    random_state=random_state_no)
        logger_object.log(file_object,'Train Test Split Successful')

    except Exception as e:
        logger_object.log(file_object,'Train Test Split Failed')
        logger_object.log(file_object,str(e))
 
    try:
        # Train the model using Random Forest Classifier
        model = RandomForestClassifier(n_estimators=n_estimate_input, criterion=criterion, class_weight=class_weight,
                                       min_samples_split=min_samples_split, max_features=max_features_input)
        model.fit(x_train, y_train)
        logger_object.log(file_object,'Model Training Successful')

    except Exception as e:
        logger_object.log(file_object,'Model Training Failed')
       
    
       # Metrics (Classification_report)
    try:
        # Predict the data
        y_pred = model.predict(x_test)
    
        cl_report=pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose()
        cl_report.to_csv(report_path,index=True)
        logger_object.log(file_object,'Classification report done')

    except Exception as e:
        logger_object.log(file_object,'Classification report failed')

    try:
        # Save the model
        pickle.dump(model,open("model/model.pkl", 'wb'))
        logger_object.log(file_object,'Saved as model.pkl successfully')

    except Exception as e:
        logger_object.log(file_object,'Saving model failed')
        logger_object.log(file_object,str(e))
    


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data=train_test(config_path=parsed_args.config)