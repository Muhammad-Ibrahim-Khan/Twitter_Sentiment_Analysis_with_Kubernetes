from train import predict
from preprocessing import cleaning_text

def get_sentiment(text):
    p_text = cleaning_text(text)
    return predict(p_text)