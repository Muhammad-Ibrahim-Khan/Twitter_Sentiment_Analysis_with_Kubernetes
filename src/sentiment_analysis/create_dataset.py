from json import loads

class TweetData():
    def __init__(self):
        self.texts = []
        self.labels = []  
    
    def update_tweet(self, text, label):
        self.texts.append(text)
        self.labels.append(label)

    def get_text(self):
        return self.texts
    
    def get_label(self):
        return self.labels

def process_data(filepath):
    Tweet = TweetData()
    with open(filepath) as f:
        for line in f:
            element = loads(line)
            Tweet.update_tweet(text=element['Text'], label=element['Target'])

    # Creating text/label dataset
    dataset_text = Tweet.get_text()
    dataset_labels = Tweet.get_label()

    return dataset_text, dataset_labels
