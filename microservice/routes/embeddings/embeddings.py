# Bundles Search Routes
# Routes related to searching for OER bundles

import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify, current_app
)
from werkzeug.exceptions import abort

#################################################
# Initialize the text embedding model
#################################################

from ...library.document_embedding import TextEmbedding

# TODO initialize text embedding model
model = TextEmbedding(language='en', model_path='./data/')

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
    if request.method == 'GET':
        # TODO retrieve the correct query parameters
        text = request.args.get('text', default='', type=str)
    elif request.method == 'POST':
        # TODO retrieve the document posted to the route
        text = request.json['text']
    else:
        return abort(405)

    # TODO write the body of the route
    return abort(501)
