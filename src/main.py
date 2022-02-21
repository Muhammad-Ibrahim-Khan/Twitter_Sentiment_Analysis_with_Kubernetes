from src.sentiment.train import predict
from src.sentiment.preprocessing import cleaning_text
from flask import Flask

def get_sentiment(text):
    print(text)
    p_text = cleaning_text(text)
    return predict(p_text)

# if __name__ == "__main__":
    # service.run(host = '0.0.0.0', port = 5000, debug = True)