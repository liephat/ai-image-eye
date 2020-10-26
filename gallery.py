import os
from flask import Flask, render_template, send_from_directory
from config.parser import ConfigParser

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)