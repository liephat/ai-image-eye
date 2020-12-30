from flask import Flask, render_template, send_from_directory, jsonify
from flask_restful import Api, Resource

from app.ui.filters import init_filters, unescape_url
from app.util.config_parser import ConfigParser
from app.util.data_reader import DataReader

app = Flask(__name__)
api = Api(app)

Config = ConfigParser()
ImageDataReader = DataReader()


class ImageData(Resource):

    def get(self, uid):
        return ImageDataReader.get_labels(uid)


api.add_resource(ImageData, "/image/data/<int:uid>")


@app.route('/')
def index():
    data = ImageDataReader.dict()
    return render_template('index.html', data=data)


@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory(Config.image_folder(), unescape_url(filename))


@app.route('/tags')
def send_tags():
    return jsonify(Config.labels('resnet').tolist())


init_filters(app)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
