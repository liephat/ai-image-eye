import os
from flask import Flask, render_template, send_from_directory, jsonify
from app.util.config_parser import ConfigParser

app = Flask(__name__,
            static_url_path='',
            static_folder='app/static',
            template_folder='app/templates')

Config = ConfigParser()


@app.route('/')
def index():
    filepaths = Config.image_files()
    images = []
    for filepath in filepaths:
        images.append(os.path.relpath(filepath, Config.image_folder()))
    return render_template('index.html', images=images)


@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory(Config.image_folder(), filename)


@app.route('/tags')
def send_tags():
    return jsonify(Config.labels('resnet').tolist())


if __name__ == '__main__':
    app.run(debug=True)
