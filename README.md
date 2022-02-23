# Twitter_Sentiment_Analysis

This project is aimed to develop a sentiment analyzer using tweets from Twitter as our input data and training two models on them to make predictions.
The pre-processing on data, word embedding model and GRU based implementation have been done seperately in the notebooks, kindly follow the format for the folder arrangement.
Details on the elements are contained in the notebooks themselves.
The .py files were created for the flask API and docker images(and containers).

## Pre-requisites

Read the requirements.txt file though pip and the necessary dependencies will be downloaded onto your virtual environment.

Another pre-requisite, especially for users on Linux, is that ensure the environment is created in conda, otherwise you'll have to also download jupyter notebook
and ipykernel in your environment before you're able to run the notebooks.

For Windows users: Simply create a conda env and import that environment in your preferred IDE for running .py files and create
and ipykernel for the notebooks.

## Notebooks

Each notebook is self-contained with all the explanations for various elements through markdown cells present.
The only thing you need to do is ensure you're running the correct environment for the notebook.

## SRC folder

This folder has all the necessary python files and code necessary to create your own API. The only thing you need to do for loading trained files through
python files is to place your 'models' folder in the 'sentiment analysis' folder within src folder.

## Flask API

The basic API configuration is present and is self-sufficient to get a response(sentiment) from your POST request at
the port you create.

## Docker

Dockerfile has the necessary configuration to build your images(you may edit if you wish so) and run your containers.
The response can, once again, be checked on the ports assigned.

## Ending note
The kind of data that can be passed to your API POST request is 'raw text data', the API will perform all the necessary 
pre-processing to make it suitable for prediction.
