import json
import os

import pytest

from app.config import parser
from app.data.ops import ImageDataHandler
from app.web.app import AppWrapper

app = AppWrapper().init_flask_app()

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

    # Add some basic image files and labels.
    # More test specific images should be created in each test individually. Otherwise,
    # many tests might have to be adjusted every time stuff is changed here.
    handler.add_label_assignment('file1.jpg', 'l_a', 'nnet', .7)
    handler.add_label_assignment('file2.jpg', 'l_a', 'nnet', .3)
    handler.add_label_assignment('file2.jpg', 'l_b', 'nnet', .5)
    handler.add_label_assignment('file3.jpg', 'l_c', 'dnet', .91,
                                 dict(l=0.1, t=0.2, r=0.3, b=0.4))
    handler.add_label_assignment('file4.jpg', 'l_a', 'user')
    handler.add_label_assignment('file4.jpg', 'l_d', 'user')

    handler.add_label_assignment('file has spaces.jpg', 'l_a', 'user')


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
