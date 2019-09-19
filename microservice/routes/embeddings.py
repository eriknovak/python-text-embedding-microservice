# Embedding Route
# Routes related to creatiung text embeddings

import sys

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify, current_app as app
)
from werkzeug.exceptions import abort


#################################################
# Initialize the text embedding model
#################################################

from ..library.text_embedding import TextEmbedding

# get model parameters
model_path = app.config['MODEL_PATH']
model_format = app.config['MODEL_FORMAT']
language = app.config['MODEL_LANGUAGE']

# initialize text embedding model
model = TextEmbedding(language=language, model_path=model_path, model_format=model_format)


#################################################
# Setup the embeddings blueprint
#################################################

bp = Blueprint('embeddings', __name__, url_prefix='/api/v1/embeddings')


@bp.route('/', methods=['GET'])
def index():
    # TODO create documentation for usage
    return abort(501)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    # assign the text placeholder
    text = None
    language = None
    if request.method == 'GET':
        # retrieve the correct query parameters
        text = request.args.get('text', default='', type=str)
        language = request.args.get('language', default=None, type=str)
    elif request.method == 'POST':
        # retrieve the text posted to the route
        text = request.json['text']
        language = request.json['language']
    else:
        # TODO: log exception
        return abort(405)

    try:
        # extract the text embedding
        text_embedding = model.text_embedding(text, language)
    except:
        # get exception
        e = sys.exc_info()[0]
        print(str(e))
        # TODO: log exception
        # something went wrong with the request
        return abort(400, message=str(e))
    else:
        # return the embedding with the text
        return jsonify({
            "language_model": model.get_language(),
            "tokens": [{ "token": t[0], "count": t[1] } for t in model.tokenize(text)],
            "embedding": text_embedding,
            "text": text
        })