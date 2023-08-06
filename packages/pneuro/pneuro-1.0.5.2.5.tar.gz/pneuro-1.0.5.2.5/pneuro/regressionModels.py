#Regression models
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score, mean_squared_error
import xgboost as xgb
from sklearn.neighbors import KNeighborsRegressor
from pneuro.appLogger import AppLogger
from pneuro.file_methods import FileOperation
import pathlib
HERE = pathlib.Path(__file__).parent
RegressionTrainingLogs = HERE/"logs"/"RegressionTrainingLogs.txt"


class RegressionModelTuner():
    """
            This class shall be used to get the best suited Regression model

            Written By: iNeuron
            Version: 1.0
            Revisions: None

    """

    def __init__(self):
        #self.file_object = open('pneuro/logs/RegressionTrainingLogs.txt', 'a+')
        self.file_object = open(RegressionTrainingLogs, 'a+')
        self.logger_object = AppLogger()
        self.file_operation = FileOperation()

    def get_tuned_knn_model(self, x_train, y_train):
        """
            Method Name : get_tuned_knn_model

            Description : This method will be used to get the hypertuned KNN Model

            x_train : Feature Columns of Training DataSet

            y_train : Target Column of Training DataSet

            output : A hyper parameter tuned model object

            Written By: Purvansh Singh

            Version : 1.0

            Revision : None
        """
        try:
            self.logger_object.log(self.file_object,
                                   "KNN Model Training Started.")
            knn_parameters = {'n_neighbors': [50, 100, 200, 250, 300, 350],
                              'weights': ['uniform', 'distance'],
                              'algorithm': ['ball_tree', 'kd_tree'],
                              'leaf_size': [20, 25, 30, 35, 40, 45, 50],
                              }
            '''
            rmdsearch = RandomizedSearchCV(KNeighborsRegressor(), knn_parameters, n_iter=10, cv=10, random_state=22,
                                           n_jobs=-1)
            rmdsearch.fit(x_train, y_train)
            hyperparameters = rmdsearch.best_params_
            n_neighbors, weights, algorithm, leaf_size = hyperparameters['n_neighbors'], hyperparameters['weights'], \
                                                         hyperparameters['algorithm'], hyperparameters['leaf_size']
            model = KNeighborsRegressor(n_neighbors=n_neighbors,
                                        weights=weights,
                                        algorithm=algorithm,
                                        leaf_size=leaf_size,
                                        n_jobs=-1)
            '''
            model = KNeighborsRegressor(n_jobs=-1)
            model.fit(x_train, y_train)
            self.logger_object.log(self.file_object,
                                   "KNN Model successfully trained.")
            return model
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in performing Model Building and Tuning. Exception message: ' + str(
                                       e))
            raise Exception()

    def get_tuned_random_forest_model(self, x_train, y_train):
        """
        Method Name: get_tuned_random_forest_classifier

        Description: This method will be used to build RandomForestRegressor model

        Input Description:

        x_train : Feature Columns of Training DataSet

        y_train : Target Column of Training DataSet

        On Failure: Raise Exception

        Written By: Purvansh Singh

        Version: 1.0

        Revisions: None

        """
        try:
            self.logger_object.log(self.file_object,
                                   "Random Forest Model Training Started.")
            self.rf_parameters = {
                'max_depth': [5, 10, 15, 20, 25, None],
                'n_estimators': range(10, 500, 50),
                'criterion': ['mse', 'mae'],
                'bootstrap': [True, False],
                'min_samples_split': range(2, 10, 1),
                'max_features': ['auto', 'log2'],
                'min_samples_leaf': range(1, 10),
            }
            '''
            self.rmdsearch = RandomizedSearchCV(RandomForestRegressor(), self.rf_parameters, n_iter=10, cv=10,
                                                random_state=22,
                                                n_jobs=-1)
            self.rmdsearch.fit(x_train, y_train)
            hyperparameters = self.rmdsearch.best_params_
            max_depth, n_estimators, criterion, bootstrap, min_samples_split, max_features, min_samples_leaf = \
                hyperparameters['max_depth'], hyperparameters['n_estimators'], hyperparameters['criterion'], \
                hyperparameters['bootstrap'], hyperparameters['min_samples_split'], hyperparameters['max_features'], \
                hyperparameters['min_samples_leaf']

            self.model = RandomForestRegressor(n_estimators=n_estimators,
                                               max_depth=max_depth,
                                               criterion=criterion,
                                               min_samples_leaf=min_samples_leaf,
                                               max_features=max_features,
                                               min_samples_split=min_samples_split,
                                               bootstrap=bootstrap,
                                               random_state=25,
                                               n_jobs=-1)
            '''
            self.model = RandomForestRegressor(n_jobs=-1)
            self.model.fit(x_train, y_train)
            self.logger_object.log(self.file_object,
                                   "Random Forest Model successfully Trained.")
            return self.model
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in performing Model Building and Tuning. Exception message: ' + str(
                                       e))
            raise Exception()

    def get_tuned_xgboost_model(self, x_train, y_train):
        """
        Method Name: get_tuned_xgboost_model

        Description: This method will be used to build XGBoost Regressor model

        Input Description:

        x_train : Feature Columns of Training DataSet

        y_train : Target Column of Training DataSet

        On Failure: Raise Exception

        Written By: Purvansh Singh

        Version: 1.0

        Revisions: None

        """
        try:
            self.logger_object.log(self.file_object,
                                   "Xgboost Model Training Started.")
            self.xg_parameters = {"n_estimators": [10, 50, 100, 200],
                                  "learning_rate": [0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
                                  "max_depth": [3, 4, 5, 6, 8, 10, 12, 15, 20],
                                  "min_child_weight": [1, 3, 5, 7],
                                  "gamma": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
                                  "colsample_bytree": [0.3, 0.4, 0.5, 0.7]
                                  }
            '''
            self.rmdsearch = RandomizedSearchCV(xgb.XGBRegressor(objective='reg:squarederror'),param_distributions=self.xg_parameters, n_iter=10, cv=10, n_jobs=-1)
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
            self.xgboost_model = xgb.XGBRegressor(n_estimators=n_estimators,
                                               learning_rate=learning_rate,
                                               gamma=gamma,
                                               min_child_weight=min_child_weight,
                                               max_depth=max_depth,
                                               colsample_bytree=colsample_bytree)
            '''
            self.xgboost_model = xgb.XGBRegressor(objective='reg:squarederror',n_jobs=-1)
            self.xgboost_model.fit(x_train, y_train)
            self.logger_object.log(self.file_object,
                                   "Xgboost Model Training Started.")
            return self.xgboost_model
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in performing Model Building and Tuning. Exception message: ' + str(
                                       e))
            raise Exception()
    def get_best_model(self,x,y):
        """
        Method Name : get_best_model

        Description : Find out the Model which has the best MSE score.

        Output: The best model name and the model object

        On Failure: Raise Exception

        Written By: iNeuron Purvansh Singh

        Version: 1.0

        Revisions: None
        """
        self.logger_object.log(self.file_object,
                               'Entered the get_best_model method of the Model_Finder class')
        try:
            train_x, test_x, train_y, test_y = train_test_split(x, y)
            #Creating Model for Xgboost
            self.xgboost = self.get_tuned_xgboost_model(train_x, train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x)

            self.xgboost_score = mean_squared_error(test_y,self.prediction_xgboost)
            self.logger_object.log(self.file_object, 'MSE for XGBoost:' + str(self.xgboost_score))

            # Creating Model for Randomforest
            self.random_forest = self.get_tuned_random_forest_model(train_x,train_y)
            self.prediction_random_forest = self.random_forest.predict(test_x)

            self.random_forest_score = mean_squared_error(test_y,self.prediction_random_forest)
            self.logger_object.log(self.file_object, 'MSE for RandomForest:' + str(self.random_forest_score))

            # Creating Model for Knn
            self.Knn = self.get_tuned_knn_model(train_x,train_y)
            self.prediction_Knn = self.Knn.predict(test_x)

            self.Knn_score = mean_squared_error(test_y, self.prediction_Knn)
            self.logger_object.log(self.file_object, 'MSE for Knn:' + str(self.Knn_score))

            if (self.xgboost_score < self.random_forest_score and self.xgboost_score < self.Knn_score):
                self.file_operation.save_model(self.xgboost,'XGBoost')
                self.train_Regression_report, self.test_regression_report = self.generate_model_report(
                self.xgboost, train_x, train_y, test_x, test_y, y.nunique())
                return 'XGBoost', self.train_Regression_report, self.test_regression_report
            elif (self.random_forest_score < self.xgboost_score and self.random_forest_score < self.Knn_score):
                self.file_operation.save_model(self.random_forest,'RandomForest')
                self.train_Regression_report, self.test_regression_report = self.generate_model_report(
                self.xgboost, train_x, train_y, test_x, test_y, y.nunique())
                return 'RandomForest', self.train_Regression_report, self.test_regression_report
            elif (self.Knn_score < self.xgboost_score and self.Knn_score < self.random_forest):
                self.file_operation.save_model(self.Knn, 'Knn')
                self.train_Regression_report, self.test_regression_report = self.generate_model_report(
                self.xgboost, train_x, train_y, test_x, test_y, y.nunique())
                return 'Knn', self.train_Regression_report, self.test_regression_report

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

                    Output : It generate training and testing of Best Model.

                    On Failure: Raise Exception

                    Written By: Purvansh Singh
                    Version: 1.0
                    Revisions: None

                """
        try:
            self.train_Regression_report = []
            self.test_regression_report = []
            train_predictions = model_object.predict(train_x)
            test_predictions = model_object.predict(test_x)
            temp_dict = {}
            temp_dict['MSE'] = mean_squared_error(train_y,train_predictions)
            temp_dict['R Squared'] = r2_score(train_y,train_predictions)
            temp_dict['RMSE'] = temp_dict['MSE']**(0.5)
            self.train_Regression_report.append(temp_dict)

            temp_dict = {}
            temp_dict['MSE'] = mean_squared_error(test_y, test_predictions)
            temp_dict['R Squared'] = r2_score(test_y, test_predictions)
            temp_dict['RMSE'] = temp_dict['MSE'] ** (0.5)
            self.test_regression_report.append(temp_dict)

            return self.train_Regression_report, self.test_regression_report
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in generate_model_report method of the ClassificationModelTuner class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the generate_model_report method of the ClassificationModelTuner class')
            raise Exception()
