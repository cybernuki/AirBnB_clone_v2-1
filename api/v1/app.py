#!/usr/bin/python3
""" create a simple web application """
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown(self):
    """ teardown the app context, calls storage.close() """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ This function handles the error 404
        error : is the error that called this function
    """
    response = {'error': 'Not found'}
    return make_response(jsonify(response), 404)

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
