import json
import logging
import base64
import os
import sys

from flask import Flask, current_app, request
from google.cloud import pubsub, vision


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


app = Flask(__name__)


app.config.update({
    'PUBSUB_VERIFICATION_TOKEN': os.environ['PUBSUB_VERIFICATION_TOKEN'],
    'PUBSUB_TOPIC': os.environ['PUBSUB_TOPIC'],
    'MESSAGING_TOPIC': os.environ['MESSAGING_TOPIC'],
    'PROJECT': os.environ['GOOGLE_CLOUD_PROJECT']
})


@app.route('/process-inventory', methods=['POST'])
def process_image():
    if current_app.config['PUBSUB_VERIFICATION_TOKEN'] != request.args.get('token', ''):
        return 'invalid request', 400

    # deserialize the envelope into a dict
    envelope = json.loads(request.data.decode('utf-8'))
    logging.debug('ENVELOPE: {}'.format(envelope))

    # eventType must be OBJECT_FINALIZE
    # if envelope['message']['attributes']['eventType'] != 'OBJECT_FINALIZE':
    #     return 'OK', 200

    # base64 decode the 'data' element in the message and deserialize into dict
    data = json.loads(base64.b64decode(envelope['message']['data']))

    # the message is not from GCS
    if data.get('kind', None) != u'storage#object':
        return 'ok', 200

    # logging.debug('OBJECT_FINALIZE: {}'.format(data['selfLink']))

    # create the gs:// path to the image
    imgpath = 'gs://{}/{}'.format(data['bucket'], data['name'])

    vis_client = vision.ImageAnnotatorClient()
    resp = vis_client.annotate_image({
        'image': {'source': {'image_uri': imgpath}},
        'features': 
            [
                {'type': vision.enums.Feature.Type.LABEL_DETECTION},
                {'type': vision.enums.Feature.Type.TEXT_DETECTION}
            ]
    })

    cps_client = pubsub.PublisherClient()
    cps_topic = 'projects/{project}/topics/{topic}'.format(
        project = current_app.config['PROJECT'],
        topic = current_app.config['MESSAGING_TOPIC']
    )

    for label in resp.label_annotations:
        if label.description == 'banana':
            logging.debug('BANANAS ARE IN STOCK')

    for text in resp.text_annotations:
        text_desc = ''.join(text.description.split())

        if text_desc == 'RESTOCKBANANAS':
            logging.debug('RESTOCKBANANAS')
            cps_client.publish(cps_topic, bytes(text_desc))

    return '', 204


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)