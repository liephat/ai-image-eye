from flask import send_from_directory

from app.data.ops import ImageDataHandler
from app.web import EndpointBase
from app.web.util.filters import unescape_url


class ImagesEndpoints(EndpointBase):
    @classmethod
    def init(cls, app):
        @app.route('/images/<filename>')
        def send_image(filename):
            return send_from_directory(cls.get_config().image_folder(), unescape_url(filename))


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


