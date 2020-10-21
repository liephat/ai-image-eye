import os
from flask import Flask, render_template, send_from_directory
from config.parser import ConfigParser

app = Flask(__name__)

Config = ConfigParser()


@app.route('/')
def index():
    filepaths = Config.image_files()
    relpaths = []
    for filepath in filepaths:
        relpaths.append(os.path.relpath(filepath, Config.image_folder()))
    return render_template('index.html', relpaths=relpaths)


@app.route('/images/<relpath>')
def send_image(relpath):
    print(relpath)
    filepath = os.path.join(Config.image_folder(), relpath)
    directory, filename = os.path.split(filepath)
    print(filepath)
    return send_from_directory(directory, filename)


if __name__ == '__main__':
    app.run(debug=True)