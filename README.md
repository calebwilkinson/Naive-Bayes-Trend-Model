# Gaussian Naive Bayes Trend Model

# Trend Model

The purpose of this project is to create a machine learning model that utilizes several features to produce a positive or
negative performance forecast for stock market indices (SPX, NDX, DJI, RUT) over 5, 10, 15, and 20 days. A Gaussian Naive
Bayes Classification model is used to train and test data. Data is pulled from Yahoo Finance using yfinance and inserts/manipulates
data for insertion into a Microsoft SQL Server.

# Author 
Caleb Wilkinson
calebwilkinson3@aol.com

# Installation
-m pip install numpy
-m pip install pandas
-m pip matplotlib
-m pip install scikit-learn
-m pip install yfinance
-m pip install pyodbc

# Directions
To get data up to date run the function update_all_data(). Once data is updated, the function model.query_user() can be used. 
This function will give you two prompts, index of choice and timeframe of choice, and then return a forecasted up or down projection
over the selected timeframe. 
