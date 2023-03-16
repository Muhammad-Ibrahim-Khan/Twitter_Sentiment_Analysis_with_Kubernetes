from os import path, mkdir

##########  PATHS ##########
TRAINED_MODEL_PATH = "src/sentiment_analysis/model/"
PATH_TO_DATASET = "src/data/clean_processed_data.json"

if not path.exists(TRAINED_MODEL_PATH):
    mkdir(TRAINED_MODEL_PATH)