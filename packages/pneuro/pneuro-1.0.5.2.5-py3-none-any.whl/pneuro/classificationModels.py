import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.model_selection import cross_val_score
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelBinarizer
from sklearn.neighbors import KNeighborsClassifier
from pneuro.appLogger import AppLogger
from pneuro.file_methods import FileOperation

import pathlib
HERE = pathlib.Path(__file__).parent
classificationTrainingLogs = HERE / "logs" / "classificationTrainingLogs.txt"


class ClassificationModelTuner():
    """
        This class shall be used to get the best suited classification model

        Written By: iNeuron
        Version: 1.0
        Revisions: None

        """

    def __init__(self):
        # self.file_object = open('pneuro/logs/classificationTrainingLogs.txt', 'a+')
        self.file_object = open(classificationTrainingLogs, 'a+')
        self.logger_object = AppLogger()
        self.file_operation = FileOperation()

    def get_tuned_random_forest_classifier(self, x_train, y_train):
        """
        Method Name: get_tuned_random_forest_classifier
        Description: This method will be used to build RandomForestClassifier model
        Input Description: It takes x_train and y_train data for training the model.

        Output:  It return Optimized RandomForestClassifier model.

        On Failure: Raise Exception

        Written By: Akhil Sagar

        Version: 1.0

        Revisions: None

        """
        try:
            self.rf_parameters = {
                'max_depth': [5, 10, 15, 20, 25, None],
                'n_estimators': range(10, 500, 50),
                'criterion': ['gini', 'entropy'],
                'bootstrap': [True, False],
                'min_samples_split': range(2, 10, 1),
                'max_features': ['auto', 'log2'],
                'min_samples_leaf': range(1, 10),
            }
            """
            self.rmdsearch = RandomizedSearchCV(RandomForestClassifier(), self.rf_parameters, n_iter=10, cv=10, random_state=22,
                                           n_jobs=-1)
            self.rmdsearch.fit(x_train, y_train)
            hyperparameters = self.rmdsearch.best_params_
            max_depth, n_estimators, criterion, bootstrap, min_samples_split, max_features, min_samples_leaf = \
            hyperparameters['max_depth'], hyperparameters['n_estimators'], hyperparameters['criterion'], \
            hyperparameters['bootstrap'], hyperparameters['min_samples_split'], hyperparameters['max_features'], \
            hyperparameters['min_samples_leaf']

            self.model = RandomForestClassifier(n_estimators=n_estimators,
                                           max_depth=max_depth,
                                           criterion=criterion,
                                           min_samples_leaf=min_samples_leaf,
                                           max_features=max_features,
                                           min_samples_split=min_samples_split,
                                           bootstrap=bootstrap,
                                           random_state=25,
                                           n_jobs=-1)
            """
            self.model = RandomForestClassifier(n_jobs=-1)
            self.model.fit(x_train, y_train)
            return self.model
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in performing Model Building and Tuning. Exception message: ' + str(
                                       e))
            raise Exception()

    def get_tuned_xgboost_classifier(self, x_train, y_train):
        """
        Method Name: get_tuned_xgboost_classifier
        Description: This method will be used to build XGBoost Classifier model
        Input Description: It takes x_train and y_train data for training the model.

        Output:  It return Optimized XGBoost model.

        On Failure: Raise Exception

        Written By: Akhil Sagar

        Version: 1.0

        Revisions: None

        """
        try:
            self.xg_parameters = {"n_estimators": [10, 50, 100, 200],
                                  "learning_rate": [0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
                                  "max_depth": [3, 4, 5, 6, 8, 10, 12, 15, 20],
                                  "min_child_weight": [1, 3, 5, 7],
                                  "gamma": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
                                  "colsample_bytree": [0.3, 0.4, 0.5, 0.7]
                                  }
            """
            self.rmdsearch = RandomizedSearchCV(XGBClassifier(objective='binary:logistic'),
                                           param_distributions=self.xg_parameters, n_iter=10, cv=10, n_jobs=-1)
            self.rmdsearch.fit(x_train, y_train)
            hyperparameters = self.rmdsearch.best_params_
            n_estimators, min_child_weight, max_depth, learning_rate, gamma, colsample_bytree = hyperparameters[
                                                                                                    'n_estimators'], \
                                                                                                hyperparameters[
                                                                                                    'min_child_weight'], \
                                                                                                hyperparameters[
                                                                                                    'max_depth'], \
                                                                                                hyperparameters[
                                                                                                    'learning_rate'], \
                                                                                                hyperparameters[
                                                                                                    'gamma'], \
                                                                                                hyperparameters[
                                                                                                    'colsample_bytree']
            self.xgboost_model = XGBClassifier(n_estimators=n_estimators,
                                          learning_rate=learning_rate,
                                          gamma=gamma,
                                          min_child_weight=min_child_weight,
                                          max_depth=max_depth,
                                          colsample_bytree=colsample_bytree)
            """
            self.xgboost_model = XGBClassifier(n_jobs=-1)
            self.xgboost_model.fit(x_train, y_train)
            return self.xgboost_model
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in performing Model Building and Tuning. Exception message: ' + str(
                                       e))
            raise Exception()

    def get_tuned_knn_classifier(self, x_train, y_train):
        """
        Method Name: get_tuned_knn_classifier
        Description: This method will be used to build KNearestNeighbour Classifier model
        Input Description: It takes x_train and y_train data for training the model.

        Output:  It return Optimized KNearestNeighbourClassifier model.

        On Failure: Raise Exception

        Written By: Akshay Anvekar


        Version: 1.0

        Revisions: None

        """
        try:
            knn_parameters = {'n_neighbors': [50, 100, 200, 250, 300, 350],
                              'weights': ['uniform', 'distance'],
                              'algorithm': ['ball_tree', 'kd_tree'],
                              'leaf_size': [20, 25, 30, 35, 40, 45, 50],
                              }
            rmdsearch = RandomizedSearchCV(KNeighborsClassifier(), knn_parameters, n_iter=10, cv=10, random_state=22,
                                           n_jobs=-1)
            rmdsearch.fit(x_train, y_train)
            hyperparameters = rmdsearch.best_params_
            n_neighbors, weights, algorithm, leaf_size = hyperparameters['n_neighbors'], hyperparameters['weights'], \
                                                         hyperparameters['algorithm'], hyperparameters['leaf_size']
            model = KNeighborsClassifier(n_neighbors=n_neighbors,
                                         weights=weights,
                                         algorithm=algorithm,
                                         leaf_size=leaf_size,
                                         n_jobs=-1)
            model.fit(x_train, y_train)
            return model
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in performing Model Building and Tuning. Exception message: ' + str(
                                       e))
            raise Exception()

    def get_best_model(self, x, y):
        """
            Method Name: get_best_model
            Description: Find out the Model which has the best AUC score.
            Output: The best model name and the model object
            On Failure: Raise Exception

            Written By: iNeuron Intelligence
            Version: 1.0
            Revisions: None

        """
        self.logger_object.log(self.file_object,
                               'Entered the get_best_model method of the Model_Finder class')
        # create best model for XGBoost
        try:
            train_x, test_x, train_y, test_y = train_test_split(x, y)

            self.xgboost = self.get_tuned_xgboost_classifier(train_x, train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x)  # Predictions using the XGBoost Model

            if len(
                    test_y.unique()) == 1:  # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)
                self.logger_object.log(self.file_object, 'Accuracy for XGBoost:' + str(self.xgboost_score))  # Log AUC
            elif len(test_y.unique()) == 2:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost)  # AUC for XGBoost
                self.logger_object.log(self.file_object, 'AUC for XGBoost:' + str(self.xgboost_score))  # Log AUC
            else:
                lb = LabelBinarizer()
                lb.fit(test_y)
                test_y_xg = lb.transform(test_y)
                self.prediction_xgboost = lb.transform(self.prediction_xgboost)
                self.xgboost_score = roc_auc_score(test_y_xg, self.prediction_xgboost)  # AUC for XGBoost
                self.logger_object.log(self.file_object, 'AUC for XGBoost:' + str(self.xgboost_score))  # Log AUC
            # create best model for Random Forest
            self.random_forest = self.get_tuned_random_forest_classifier(train_x, train_y)
            self.prediction_random_forest = self.random_forest.predict(
                test_x)  # prediction using the Random Forest Algorithm

            if len(
                    test_y.unique()) == 1:  # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.random_forest_score = accuracy_score(test_y, self.prediction_random_forest)
                self.logger_object.log(self.file_object, 'Accuracy for RF:' + str(self.random_forest_score))
            elif len(test_y.unique()) == 2:
                self.random_forest_score = roc_auc_score(test_y, self.prediction_random_forest)  # AUC for Random Forest
                self.logger_object.log(self.file_object, 'AUC for RF:' + str(self.random_forest_score))
            else:
                lb = LabelBinarizer()
                lb.fit(test_y)
                test_y_rf = lb.transform(test_y)
                self.prediction_random_forest = lb.transform(self.prediction_random_forest)
                self.random_forest_score = roc_auc_score(test_y_rf,
                                                         self.prediction_random_forest)  # AUC for Random Forest
                self.logger_object.log(self.file_object, 'AUC for RF:' + str(self.random_forest_score))

            if (self.random_forest_score < self.xgboost_score):
                self.file_operation.save_model(self.xgboost, 'XGBoost')
                self.train_classification_report, self.test_classification_report = self.generate_model_report(
                    self.xgboost, train_x, train_y, test_x, test_y, y.nunique())
                return 'XGBoost', self.train_classification_report, self.test_classification_report
            else:
                self.file_operation.save_model(self.random_forest, 'RandomForest')
                self.train_classification_report, self.test_classification_report = self.generate_model_report(
                    self.random_forest, train_x, train_y, test_x, test_y, y.nunique())
                return 'RandomForest', \
                       self.train_classification_report, self.test_classification_report

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()

    def generate_model_report(self, model_object, train_x, train_y, test_x, test_y, num_classes):
        """
                    Method Name: generate_model_report
                    Description: Find out the Model which has the best AUC score.
                    Output: The best model name and the model object
                    On Failure: Raise Exception

                    Written By: iNeuron Intelligence
                    Version: 1.0
                    Revisions: None

                """
        try:
            self.train_classification_report = []
            self.test_classification_report = []
            train_predictions = model_object.predict(train_x)
            test_predictions = model_object.predict(test_x)
            train_report = classification_report(train_y, train_predictions).split()[4:]
            test_report = classification_report(test_y, test_predictions).split()[4:]
            counter = 0
            while len(self.train_classification_report) < num_classes + 1:
                temp_dict = {}
                temp_dict['class'] = train_report[counter]
                temp_dict['precision'] = train_report[counter + 1]
                temp_dict['recall'] = train_report[counter + 2]
                temp_dict['f1-score'] = train_report[counter + 3]
                temp_dict['support'] = train_report[counter + 4]
                counter = counter + 5
                self.train_classification_report.append(temp_dict)
            counter = 0
            while len(self.test_classification_report) < num_classes + 1:
                temp_dict = {}
                temp_dict['class'] = test_report[counter]
                temp_dict['precision'] = test_report[counter + 1]
                temp_dict['recall'] = test_report[counter + 2]
                temp_dict['f1-score'] = test_report[counter + 3]
                temp_dict['support'] = test_report[counter + 4]
                counter = counter + 5
                self.test_classification_report.append(temp_dict)

            return self.train_classification_report, self.test_classification_report
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in generate_model_report method of the ClassificationModelTuner class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the generate_model_report method of the ClassificationModelTuner class')
            raise Exception()
