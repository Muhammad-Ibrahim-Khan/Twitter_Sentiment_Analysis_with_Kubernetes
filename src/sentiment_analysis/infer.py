import tensorflow as tf
from src.utils.constants import TRAINED_MODEL_PATH
from src.sentiment_analysis.preprocess_data import clean_text
from src.sentiment_analysis.train import BaseModel

class SentimentAnalysisModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.trained_model_path = TRAINED_MODEL_PATH
        self.kmodel = self.load_model()
    
    def load_model(self):
        try:
            return tf.keras.models.load_model(self.trained_model_path)
        except Exception:
            BaseModel.train_and_save_model(self)
            return tf.keras.models.load_model(self.trained_model_path)

    def predict(self, text_list):
        if isinstance(text_list, str):
            text_list = [text_list]
        
        # Clean input text
        clean_text_list = [clean_text(text) for text in text_list]
        print(text_list[0])
        labels = self.kmodel.predict(clean_text_list)
        return [
            {
                "Text": text,
                "Sentiment": "Positive" if label >= 0.5 else "Negative",
                "Label": str(label[0])
            }
            for text, label in zip(text_list, labels)
        ]
