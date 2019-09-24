# Embedding Route
# Routes related to creatiung text embeddings

import os
import sys
import ast
from requests import post

from flask import (
    Blueprint, flash, g, request, jsonify, current_app as app, render_template, url_for
)
from werkzeug.exceptions import abort

from langdetect import detect

#################################################
# Setup the proxy configuration
#################################################

proxy_config = app.config["PROXY"]

#################################################
# Setup the index blueprint
#################################################

bp = Blueprint('index', __name__)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@bp.route('/', methods=['GET'])
def index():
    # get the documentation information
    MODEL_LANGUAGES = [lang for lang in proxy_config.keys()]
    HOST = app.config['HOST'] if 'HOST' in app.config else '127.0.0.1'
    PORT = app.config['PORT'] if 'PORT' in app.config else '5000'

    result = {
        "model_languages": MODEL_LANGUAGES,
        "host": HOST,
        "port": PORT
    }

    # render the documentation
    return render_template('index.html', result=result)


@bp.route('/embeddings', methods=['GET', 'POST'])
def embedding():
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
        text_language = language if language != None else detect(text)
        # check if we have a service that is able to handle the language
        if text_language not in proxy_config.keys():
            # return the error message
            return jsonify({
                "error": {
                    "message": "Unsupported language: '{}'".format(text_language),
                },
                "languages": {
                    "supported": [lang for lang in proxy_config.keys()]
                }
            })

        # setup the post request information
        HOST = '127.0.0.1'
        PORT = proxy_config[text_language]

        # assign the data to send to the appropriate service
        data = {
            "text": text,
            "language": text_language
        }
        # make the post request
        r = post(f"http://{HOST}:{PORT}/api/v1/embeddings/create", json=data)
        # return the content
        return jsonify(r.json())

    except:
        # get exception
        e = sys.exc_info()[0]
        # TODO: log exception
        # something went wrong with the request
        return abort(400)
