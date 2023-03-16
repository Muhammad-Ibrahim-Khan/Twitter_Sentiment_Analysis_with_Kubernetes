# Imports
import os
import tensorflow as tf
from keras import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
from keras.layers import TextVectorization
from src.sentiment_analysis.config import train_config
from src.utils.constants import TRAINED_MODEL_PATH, PATH_TO_DATASET
from src.sentiment_analysis.create_dataset import process_data

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class BaseModel():
    def __init__(self) -> None:
        self.trained_model_path = TRAINED_MODEL_PATH
        self.dataset_path = PATH_TO_DATASET

    def train_and_save_model(self):
        text, labels = process_data(filepath=PATH_TO_DATASET)
        text_tensor = tf.convert_to_tensor(text)
        labels_tensor = tf.convert_to_tensor(labels)
        
        # Creating dataset for our TextVectorizer layer
        p_text = tf.data.Dataset.from_tensors(text_tensor)

        # Text Vectorization
        vectorize_layer = TextVectorization(standardize='lower_and_strip_punctuation',
                                        max_tokens=train_config.get("VOCAB_SIZE"),
                                        split='whitespace',
                                        output_mode='int',
                                        output_sequence_length=train_config.get("SEQUENCE_LEN"))

        vectorize_layer.adapt(p_text)

        # Create Model
        model = Sequential([
            vectorize_layer,
            Embedding(train_config.get("VOCAB_SIZE"), train_config.get("EMBEDDING_DIM"),
            name='embedding'),
            GlobalAveragePooling1D(),
            Dense(train_config.get("DENSE_NODES"), activation='relu'),
            Dense(1, activation='sigmoid') # We want either 0 or 1 for our sentiment analysis
        ])

        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir='logs') # Saving statistics for tensorboard

        # Compiling and training model
        model.compile(optimizer=train_config.get("OPTIMIZER"),
                    loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
                    metrics=train_config.get("METRICS"))

        model.fit(x=text_tensor,
                y=labels_tensor,
                batch_size=train_config.get("BATCH_SIZE"),
                epochs=train_config.get("EPOCHS"), 
                validation_split=0.1,
                callbacks=[tensorboard_callback])
        
        model.save(self.trained_model_path)
