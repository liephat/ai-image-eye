import json
import os

import pytest

from app.__main__ import app
from app.config import parser
from app.data.ops import ImageDataHandler

TEST_DATABASE = "test_image_label.db"
TEST_SETTINGS = {
    "images": {
        "folder": "images",
        "formats": ["jpg", "arw"]
    },
    "labeling": {
        "resnet": {
            "model": "config/models/resnet/resnet50-v2-7.onnx",
            "labels": "config/models/resnet/imagenet-simple-labels.json"
        }
    },
    "data": {
        "file": TEST_DATABASE
    }
}
TEST_SETTINGS_FILE = 'tests/test_settings.json'


def _setup_test_settings():
    with open(TEST_SETTINGS_FILE, 'w') as f:
        json.dump(TEST_SETTINGS, f, indent=4)
    parser.FILE = TEST_SETTINGS_FILE


def _fill_test_database():
    handler = ImageDataHandler
    handler.reset()

    if os.path.isfile(TEST_DATABASE):
        os.unlink(TEST_DATABASE)

    handler.add_new_image('file1.jpg', ['a', 'b', 'c'])
    handler.add_new_image('file2.jpg', ['a', 'b', 'c'])
    handler.add_new_image('file3.jpg', ['c'])
    handler.add_new_image('file4.jpg', ['a', 'd'])
    handler.add_new_image('file has spaces.jpg', ['a', 'b', 'c', 'd'])


@pytest.fixture
def client():
    """ Basic test fixture for our Flask app

    Will magically be used by any test function that has a 'client' parameter.
    See https://flask.palletsprojects.com/en/1.1.x/testing/ for details.
    """
    app.config['TESTING'] = True
    _setup_test_settings()
    _fill_test_database()

    with app.test_client() as client:
        yield client
