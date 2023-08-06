import os

from pneuro.file_methods import FileOperation
from pneuro.appLogger import AppLogger
from pneuro.preProcess import Preprocessor
import pathlib
HERE = pathlib.Path(__file__).parent
predictionLogs = HERE / "logs" / "predictionLogs.txt"


class CustomException(Exception):
    pass

class Prediction():
    """
        This class shall  be used for prediction.

        Written By: iNeuron Intelligence
        Version: 1.0
        Revisions: None

        """

    def __init__(self):
        """
                        Method Name: __init__
                        Description: This method is for attributes initialization
                        Output: attributes

                        Written By: iNeuron Intelligence
                        Version: 1.0
                        Revisions: None

                """
        #self.file_object = open('pneuro/logs/predictionLogs.txt', 'a+')
        self.file_object = open(predictionLogs, 'a+')
        self.logger = AppLogger()
        self.file_operation = FileOperation()
        self.models_directory = 'models'
        self.preprocessor = Preprocessor()

    def predict_results(self, data, target_column, orig_data_col,unwanted_cols):
        """
            Method Name: predict_results
            Description: This method is for predicting the results of the test data
            Output: attributes
            Written By: iNeuron Intelligence
            Version: 1.0
            Revisions: None
      """
        model_name = os.chdir(self.models_directory)
        model_file_name = os.listdir()[0]
        os.chdir('../')
        #loading the best model from the directory
        model = self.file_operation.load_model(model_file_name)
        #adding the dummy target column for preprocessing the predict data
        data[target_column]=0
        difList = [string for string in orig_data_col if string not in data.columns]
        print(difList)
        #if len(difList)>0:
            #self.logger.log(self.file_object,
            #                       'The predict data structure is differing from trained data structure')
            #raise RuntimeError("The predict data structure is differing from trained data structure. Please provide valid data ")
        try:
            #preprocess the data
            x= self.preprocessor.preprocess(data, target_column,unwanted_cols, process='predict')
            self.logger.log(self.file_object,
                                   'Preprocessing the data to be predicted')
        except Exception as e:
            self.logger.log(self.file_object,
                                   'E : Exception occured during Preprocessing of Predictable Data' + str(
                                       e))
            raise Exception()
        self.logger.log(self.file_object,
                               'After preprocessing the data to be predicted')
        try:
            #x=x.drop(columns=target_column)
            results = model.predict(x)
            data[target_column] = results
        except Exception as e:
            self.logger.log(self.file_object,
                                   'E : Exception occured during predicting the data after preprocessing' + str(
                                       e))
            raise Exception()
        self.logger.log(self.file_object,
                               'Model Prediction completed')
        return data
