import logging

from flask import Flask, render_template, send_from_directory, jsonify
from flask_restful import Api, Resource

from app.data.ops import ImageDataHandler
from app.ui.filters import init_filters, unescape_url
from app.config.parser import ConfigParser


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

# Load application configurations
config = ConfigParser()
image_data = ImageDataHandler()

@app.route('/')
def index():
    return render_template('index.html', images=image_data.filelist())


@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory(config.image_folder(), unescape_url(filename))


@app.route('/all_images')
def all_images():
    return {
        'images': [
            {
                'path': f'images/{filename}',
                'uid': filename,
            } for filename in image_data.filelist()
        ]
    }


init_filters(app)

if __name__ == '__main__':
    logger.info('Starting up ... welcome to flask-image-gallery')
    app.run(debug=True, port=5000)
