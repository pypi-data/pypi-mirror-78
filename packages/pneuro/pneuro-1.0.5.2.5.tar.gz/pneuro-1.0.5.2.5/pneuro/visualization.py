import scipy
from scipy.stats.stats import pearsonr
from datetime import datetime
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from pneuro.appLogger import AppLogger
import pathlib
HERE = pathlib.Path(__file__).parent
dataVisualizationLogs = HERE/"logs"/"dataVisualizationLogs.txt"


class DataVisualization:
    """
    This class shall be used to include all Data Visualization techniques to be feed to the Machine Learning Models

    Written By: Shakti Kumar
    Version: 1.0
    Revisions: None

    """

    def __init__(self):
        #self.file_object = open('pneuro/logs/dataVisualizationLogs.txt', 'a+')
        self.file_object = open(dataVisualizationLogs, 'a+')
        self.logger_object = AppLogger()

    def balance_imbalance_check(self, dataframe, target):

        """
        Method Name: balance_imbalance_check
        Description: This method will be used to plot the balance/imbalance datasets using barplot/countplot

        Input Description: data: the input dataframe with target column.
                           target: target column name.

        Output: plot of target variable value count.
        On Failure: Raise Exception

        Written By: shakti kumar
        Version: 1.0
        Revisions: None

        """

        try:
            # x = sns.countplot(target,data=dataframe).set_title("Balance Imbalance Count")
            # sns.barplot(x = 'is_promoted', y = 'is_promoted' ,data=df, hue  = 'is_promoted', estimator = lambda x: len(x)/len(df) *100).set_title("Balance Imbalance Count")
            # sns.barplot(x='is_promoted', y='is_promoted', data=dataframe,
            #             estimator=lambda x: len(x) / len(dataframe) * 100)
            # plt.xlabel('ispromoted')
            # plt.ylabel('percentage')
            # plt.title('Balance Imbalance Count')
            # plt.savefig("static/graphs/imbalance.png")
            print(list(target.value_counts().index))
            print((target.value_counts().iloc[:,0]))
            plotdata=[go.Bar(
                data=dataframe,
                x=list(target.value_counts().index),
                y= (target.value_counts())
            )]
            graphJSON = json.dumps(plotdata, cls=plotly.utils.PlotlyJSONEncoder)

            return graphJSON
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in checking balance and imbalance of the target(Graphically). Exception message: ' + str(
                                       e))  # Logging the exception message
            self.logger_object.log(self.file_object,
                                   'Target Value balance and imbalance check fail.Exited the balance_imbalance_check method of the DataVisualization class')  # Logging unsuccessful load of data
            raise Exception()  # raising exception and exiting

    def correlation_heatmap(self, dataframe):

        """
        Method Name: correlation_heatmap
        Description: This method will be used to generate interactive heatmap plot to show the pairwise correlation of input variables

        Input Description: data: the input dataframe with target column.
        Output: returns json file with correlation information that can be used by plotly to generate interactive plots.
        On Failure: Raise Exception

        Written By: Shashank Prakash
        Version: 1.0
        Revisions: None

        """
        self.logger_object.log(self.file_object,'Entered corelation heat map method')
        try:

            data = dataframe.select_dtypes(include=[np.number])

            #plt.figure(figsize=(20, 10))
            #sns.set_palette("PuBuGn_d")
            #plot = sns.heatmap(data.corr(), annot=True, cmap='RdYlGn')
            #plot.figure.savefig("static/graphs/correlation.png")

            plotdata = [go.Heatmap(
                z=data.corr(),
                x=list(data.columns),
                y=list(data.columns)
                ,dx=1,dy=1
                )]
            
            graphJSON = json.dumps(plotdata, cls=plotly.utils.PlotlyJSONEncoder)
            self.logger_object.log(self.file_object, 'Exited corelation heat map method')

            return graphJSON

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in plotting correlation heatmap. Exception message: ' + str(
                                       e))  # Logging the exception message
            self.logger_object.log(self.file_object,
                                   'Plotting of heatmap fails.Exited the correlation_heatmap method of the DataVisualization class')  # Logging unsuccessful load of data
            raise Exception()  # raising exception and exiting
