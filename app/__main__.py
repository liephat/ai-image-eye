import logging

from app.web.app import AppWrapper

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app = AppWrapper().init_flask_app()
    # FIXME: threaded=False is a workaround for SQLAlchemy problems with sessions in multiple
    # threads
    app.run(debug=True, port=5000, threaded=False)
