import json
import logging
import base64
import os
import firebase_admin
import requests

from flask import Flask, current_app, request
from google.cloud import pubsub
from firebase_admin import messaging


app = Flask(__name__)


app.config.update({
    'PUBSUB_VERIFICATION_TOKEN': os.environ['PUBSUB_VERIFICATION_TOKEN'],
    'PUBSUB_TOPIC': os.environ['PUBSUB_TOPIC'],
    'PROJECT': os.environ['GOOGLE_CLOUD_PROJECT'],
    'METADATA_SERVER': os.environ['METADATA_SERVER']
})


firebase_app = firebase_admin.initialize_app()


@app.route('/process-message', methods=['POST'])
def process_message():
    if current_app.config['PUBSUB_VERIFICATION_TOKEN'] != request.args.get('token', ''):
        return 'invalid request', 400

    # deserialize the envelope into a dict
    envelope = json.loads(request.data.decode('utf-8'))
    logging.debug('ENVELOPE: {}'.format(envelope))

    # base64 decode the 'data' element in the message
    data = base64.b64decode(envelope['message']['data'])

    if data == 'RESTOCKBANANAS':
        # query the metadata server for the staff app token
        metadata = requests.get(
            current_app.config['METADATA_SERVER'], 
            headers={'Metadata-Flavor': 'Google'}
        )
        push_token = metadata.json()['attributes']['staff-app-token']

        logging.debug('PUSH TOKEN: {}'.format(push_token))

        message = messaging.Message(
            data = {
                'msg': 'Time to restock the bananas'
            },
            token = push_token
        )
        response = messaging.send(message)
        logging.debug('SEND: {}'.format(message.__dict__))
        logging.debug('RESP: {}'.format(response))

    return '', 204


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)