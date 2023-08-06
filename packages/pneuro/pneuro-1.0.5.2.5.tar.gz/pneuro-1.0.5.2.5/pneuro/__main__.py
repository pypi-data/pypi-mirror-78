from flask import Flask, render_template, request
import pandas as pd
import json

from pneuro.data_loader import DataGetter
from pneuro.preProcess import Preprocessor
from pneuro.visualization import DataVisualization
from pneuro.classificationModels import ClassificationModelTuner
from pneuro.regressionModels import RegressionModelTuner
from pneuro.predict import Prediction


app = Flask(__name__)

# All class instantiation
data_getter = DataGetter()
preprocessor = Preprocessor()
visuals = DataVisualization()
classification_model = ClassificationModelTuner()
regression_model = RegressionModelTuner()
prediction = Prediction()


@app.route('/', methods=['GET'])
def index():
    """
                              Method Name: index
                              Description: starting point of app.py code which redirect you to the index.html page
                              where you can select the format of data and upload it for further process
                              Output: index html page.
                              On Failure: Raise Exception

                              Written By: iNeuron Intelligence
                              Revisions: None

                              """
    return render_template('index.html')


@app.route('/load_data', methods=['POST'])
def load_data_from_source():
    """
                                Method Name: load_data_from_source
                                Description: describes data frame infomation as below:
                                             	The number of rows
                                             	The number of columns
                                             	Number of missing values per column and their percentage
                                             	Total missing values and it’s percentage
                                             	Number of categorical columns and their list
                                             	Number of numerical columns and their list
                                             	Number of duplicate rows
                                             	Number of columns with zero standard deviation and their list
                                                 Size occupied in RAM

                                Output: tables.html page
                                On Failure: Raise Exception

                                Written By: iNeuron Intelligence
                                Revisions: None

                              """
    try:
        file = request.files['filename'] #File can be obtained from request.files
        file_type = request.form['source'] #File Source can be obtained here
        # print(file,file_type)
        if request.form['delimiter'] is not None:
            delimeter = str(request.form['delimiter'])
        global dataset    #Declare global variable
        data_getter = DataGetter()  # instantiation for genrating preprocessing logs
        dataset = data_getter.get_data(file_type, file,delimeter)   #call get_data method, it will load the dataset into dataframe
        preprocessor = Preprocessor()  # instantiation for genrating preprocessing logs
        data_profile = preprocessor.get_data_profile(dataset)  #call get_data_profile
        # print(data.head())
        # render template tables.html with the respective dataset

    except Exception as e:
        return render_template("index.html",message="No file selected")
    return render_template('tables.html', tables=[dataset.head(10).to_html(classes='data', header="True")],
                               columns=dataset.columns, profile=data_profile)


@app.route('/start_processing', methods=['POST'])
def start_processing():
    """
                                  Method Name: start_processing
                                  Description: receive the problem type and target column and unwanted columns from tables
                                  html page,generates the correlation table and different types of plots
                                  Output: charts.html page
                                  On Failure: Raise Exception

                                  Written By: iNeuron Intelligence
                                  Revisions: None

                                  """

    global problem_type, target_column, unwanted_cols
    problem_type = request.form['problem_type'] #get problem_type, that can be classification or regression
    target_column = request.form['target_column']   #get target column name
    try:
        unwanted_cols = request.form['unwanted_cols']   #get unwanted columns
    except:
        unwanted_cols=None
    global x, y
    preprocessor = Preprocessor()  # instantiation for genrating prediction logs
    x, y = preprocessor.preprocess(dataset, target_column,unwanted_cols)  #Calling preprocess method of preprocessor class
    hmap=visuals.correlation_heatmap(x)
    #balance_plot=visuals.balance_imbalance_check(x,y)
    return render_template('charts.html', hmap=hmap,  balance_plot=hmap)


@app.route('/build_model', methods=['POST'])
def build_model():
    """
                                       Method Name: build_model
                                       Description:generates the performance report of both the test and train data
                                       for both the classification and regression problems
                                       Output: model_report.html page in case if any thing fails inside the if condition
                                       then index.html age is returned
                                       On Failure: Raise Exception

                                       Written By: iNeuron Intelligence
                                       Revisions: None

                                       """
    #if problem type is classification, then get the best model with the classification report, else render index.html
    if problem_type == 'Classification':
        model_name, train_classification_report, test_classification_report = classification_model.get_best_model(x, y)
        return render_template('model_report_classification.html', model_name=model_name,
                               train_report=train_classification_report[:len(train_classification_report) - 1],
                               test_report=test_classification_report[:len(test_classification_report) - 1])
    else:
        model_name,train_reg_report,test_reg_report = regression_model.get_best_model(x, y)

        return render_template('model_report_regression.html', model_name=model_name,
                               train_report=train_reg_report,
                               test_report=test_reg_report)


@app.route('/try_prediction', methods=['POST'])
def try_predict():
    """
                                       Method Name: try_predict
                                       Description: provides the html page for providing the data for prediction,give your prediction data here.
                                       Output: prediction.html page
                                       On Failure: Raise Exception

                                       Written By: iNeuron Intelligence
                                       Revisions: None

                                       """
    return render_template('prediction.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
                                       Method Name: predict
                                       Description: takes the prediction data from prediction.html page
                                       and perform same kind of transformation as the train  and test data set
                                       and provides prediction result
                                       Output: prediction_results.html page
                                       On Failure: Raise Exception

                                       Written By: iNeuron Intelligence
                                       Revisions: None

                                       """
    global prediction_dataset
    try:
        file = request.files['prediction_filename'] #get prediction file
        file_type = request.form['source']  #get file type
        if request.form['delimiter'] is not None:
            delimeter = str(request.form['delimiter'])
        prediction_dataset = data_getter.get_data(file_type, file, delimeter) #Matching with function definition
    except:
        try:
            json_data=json.loads(request.form['pred_request'])

            prediction_dataset= pd.read_json(json_data)
        except:
            json_data=None
    preds = prediction.predict_results(prediction_dataset,target_column,x.columns,unwanted_cols)  #predict the result for the data loaded

    #render prediction_results.html with the prediction result
    return render_template('prediction_results.html', tables=[preds.head(10).to_html(classes='data', header="True")],
                           columns=preds.columns)


def main():
	app.run(debug=True)

if __name__ == '__main__':
	main()
