# Imports
import tensorflow as tf
import json
from keras import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
from keras.layers import TextVectorization

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Setting Hyper-parameters
BATCH_SIZE = 1024
SEED = 123
DENSE_NODES = 16
OPTIMIZER = 'adam'
METRICS = ['accuracy']
EPOCHS = 5
VOCAB_SIZE = 10000
SEQUENCE_LEN = 50
EMBEDDING_DIM = 16
LOAD_MODEL = True
model_loc = 'src/models/tf_word_em'

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
    

if LOAD_MODEL:
    model = tf.keras.models.load_model(model_loc)

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
                                    max_tokens=VOCAB_SIZE,
                                    split='whitespace',
                                    output_mode='int',
                                    output_sequence_length=SEQUENCE_LEN)

    vectorize_layer.adapt(p_text)

    # Create Model
    model = Sequential([
        vectorize_layer,
        Embedding(VOCAB_SIZE, EMBEDDING_DIM,
         name='embedding'),
        GlobalAveragePooling1D(),
        Dense(DENSE_NODES, activation='relu'),
        Dense(1, activation='sigmoid') # We want either 0 or 1 for our sentiment analysis
    ])

    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir='logs') # Saving statistics for tensorboard

    # Compiling and training model
    model.compile(optimizer=OPTIMIZER,
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
                metrics=METRICS)

    model.fit(x=ds_text,
            y=ds_labels,
            batch_size=BATCH_SIZE,
            epochs=EPOCHS, 
            validation_split=0.1,
            callbacks=[tensorboard_callback])

# Function for making predictions
def predict(input_text):

    label = model.predict([input_text])

    if label >= 0.5:
        return "Positive Sentiment"
    else:
        return "Negative Sentiment"
