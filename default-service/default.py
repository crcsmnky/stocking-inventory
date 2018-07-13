import os

from flask import Flask


app = Flask(__name__)


app.config.update({
    'PROJECT': os.environ['GOOGLE_CLOUD_PROJECT']
})


@app.route('/', methods=['GET'])
def index():
    return 'Hello Google Cloud Next 2018!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)