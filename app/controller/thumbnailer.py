import logging
import os
import typing

import cv2

from app.data.ops import ImageDataHandler

if typing.TYPE_CHECKING:
    from app.data.models import Image


logger = logging.getLogger(__name__)

class Thumbnailer:

    _cache_dir = None

    @classmethod
    def _get_cache_directory(cls):
        if cls._cache_dir is None:
            cls._cache_dir = os.path.join(os.getenv('XDG_CACHE_HOME',
                                                    os.path.join(os.getenv('HOME'), '.cache')),
                                          'flask-image-gallery', 'thumbnails')
            logger.info(f'Using thumbnail cache dir "{cls._cache_dir}"')
        return cls._cache_dir

    @classmethod
    def _get_thumbnail_path(cls, image_id):
        if not os.path.isdir(cls._get_cache_directory()):
            os.makedirs(cls._get_cache_directory())
        return os.path.join(cls._get_cache_directory(), f'{image_id}.jpg')

    @classmethod
    def get_thumbnail_url(cls, image: 'Image'):
        return f'thumbnails/{image.image_id}'

    @classmethod
    def get_thumbnail(cls, image_id, image_base_path):
        thumbnail_path = cls._get_thumbnail_path(image_id)
        if not os.path.isfile(thumbnail_path):
            image = ImageDataHandler.get_image(image_id)
            cls._create_resized_image(os.path.join(image_base_path, image.file), thumbnail_path,
                                      290)
        return thumbnail_path

    @classmethod
    def _create_resized_image(cls, src_path, dest_path, width):
        image_data = cv2.imread(src_path)
        factor = width / image_data.shape[1]
        height = round(image_data.shape[0] * factor)
        resized_image = cv2.resize(image_data, (width, height), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(dest_path, resized_image)




