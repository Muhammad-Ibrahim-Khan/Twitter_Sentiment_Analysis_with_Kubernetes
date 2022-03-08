# Twitter Sentiment Analysis

This project is aimed to develop a sentiment analyzer using tweets from Twitter as our input data and training two models on them to make predictions.
The pre-processing on data, word embedding model and GRU based implementation have been done seperately in the notebooks, kindly follow the format for the folder arrangement.
Details on each individual element is present in the notebooks.
The .py files were created for the flask API and docker images(and containers).

## Pre-requisites

Run the following line on your terminal for downloading the necessary dependencies into your virtual environment.

> pip install -r requirements.txt

Another pre-requisite, especially for users on Linux, is that ensure the environment is created in conda, otherwise you'll have to also download jupyter notebook
and ipykernel in your environment before you're able to run the notebooks.

For Windows users: Simply create a virtual environment and import that environment in your preferred IDE for running .py files and create
an ipykernel for the notebooks.

## Notebooks

Each notebook is self-contained with all the explanations for various elements through markdown cells present with their associated figures and links.

## Flask API

The basic API configuration is present and is self-sufficient to get a response(sentiment) from your POST request at
the port you create.

## Docker

Dockerfile has the necessary configuration to build your images and run your containers.
