
import logging

from app.web.app import AppWrapper

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)


app = AppWrapper().init_flask_app()
