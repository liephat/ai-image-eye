import logging

from flask import Flask, render_template, send_from_directory

from app.api import RestApi
from app.config.parser import ConfigParser
from app.data.ops import ImageDataHandler
from app.ui.filters import init_filters, unescape_url


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load application configurations
config = ConfigParser()

@app.route('/')
def index():
    return render_template('index.html', images=ImageDataHandler.filelist())


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
            } for filename in ImageDataHandler.filelist()
        ]
    }


init_filters(app)
RestApi.init(app)
logger.info('Starting up ... welcome to flask-image-gallery')
logger.debug(f'\n{app.url_map}')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
