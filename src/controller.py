import traceback

from src.main import get_sentiment

import json
from flask import Blueprint, request, Response

from flask_cors import cross_origin

process = Blueprint('process', __name__)

@process.route('/tweet', methods=['POST'])
@cross_origin()
def sentiment_analysis():
    try:

        # if len(request.text) == 0:
        #     return Response(
        #         response=json.dumps({"error":"Missing input text."}),
        #         status=400,
        #         mimetype="application/text"
        #     )

        # else:
        text = request.data.decode("utf-8")
        sentiment = get_sentiment(text)
        
        return Response(response=json.dumps(sentiment), 
            status=200,
            mimetype="application/text"
        )
    
    except Exception as e:
        print(traceback.format_exc())
        return Response(response=str(e),
            status=400,
            mimetype="application/text"
            )


