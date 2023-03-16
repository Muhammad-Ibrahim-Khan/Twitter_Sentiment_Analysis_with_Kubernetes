from flask import Flask, request, jsonify
from flask_cors import CORS
from src.sentiment_analysis.infer import SentimentAnalysisModel
from src.app_config import flask_config

# Flask App configuration
app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = flask_config.get("DEBUG_MODE")

Model = SentimentAnalysisModel()

@app.route('/get_sentiments', methods=["POST"])
def get_sentiments():
    texts = request.get_json()
    return jsonify(Model.predict(texts.get("tweets")))

if __name__ == "__main__":
    app.run(host = flask_config.get("HOST"), port = flask_config.get("PORT"))