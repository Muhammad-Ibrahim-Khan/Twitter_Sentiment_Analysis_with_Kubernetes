# Imports
import tensorflow as tf
import json
from keras import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
from keras.layers import TextVectorization

import config_train
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Creating Tweet Class
class Tweet():
    def __init__(self, text, label):
        self.text = text
        self.label = label

class Utils():
    def __init__(self, tweets):
        self.tweets = tweets
        
    def get_text(self):
        return [x.text for x in self.tweets]
    
    def get_label(self):
        return [x.label for x in self.tweets]
    

# Hyperparameters located in config_train.py

if config_train.LOAD_MODEL:
    model = tf.keras.models.load_model('/home/mik/TSA/models/tf_word_em')

else:
    # Reading pre-processed data
    file_name = '../../data/Data_processed.json'

    tweets = []
    with open(file_name) as f:
        for line in f:
            tweet = json.loads(line)
            tweets.append(Tweet(tweet['Text'], tweet['Target']))

    # Creating text/label dataset
    dataset_text = Utils(tweets).get_text()
    dataset_labels = Utils(tweets).get_label()

    ds_labels = tf.convert_to_tensor(dataset_labels)
    ds_text = tf.convert_to_tensor(dataset_text)

    # Creating dataset for our TextVectorizer layer
    p_text = tf.data.Dataset.from_tensors(ds_text)

    # Text Vectorization
    vectorize_layer = TextVectorization(standardize='lower_and_strip_punctuation',
                                    max_tokens=config_train.VOCAB_SIZE,
                                    split='whitespace',
                                    output_mode='int',
                                    output_sequence_length=config_train.SEQUENCE_LEN)

    vectorize_layer.adapt(p_text)

    # Create Model
    model = Sequential([
        vectorize_layer,
        Embedding(config_train.VOCAB_SIZE, config_train.EMBEDDING_DIM,
         name='embedding'),
        GlobalAveragePooling1D(),
        Dense(config_train.DENSE_NODES, activation='relu'),
        Dense(1, activation='sigmoid') # We want either 0 or 1 for our sentiment analysis
    ])

    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir='logs') # Saving statistics for tensorboard

    # Compiling and training model
    model.compile(optimizer=config_train.OPTIMIZER,
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
                metrics=config_train.METRICS)

    model.fit(x=ds_text,
            y=ds_labels,
            batch_size=config_train.BATCH_SIZE,
            epochs=config_train.EPOCHS, 
            validation_split=0.1,
            callbacks=[tensorboard_callback])

# Function for making predictions
def predict(input_text):

    label = model.predict([input_text])

    if label >= 0.5:
        return "Positive Sentiment"
    else:
        "Negative Sentiment"
