from flask import send_from_directory, make_response, send_file, request

from app.controller.thumbnailer import Thumbnailer
from app.data.ops import ImageDataHandler
from app.web import EndpointBase
from app.web.util.filters import unescape_url


class ImagesEndpoints(EndpointBase):
    @classmethod
    def init(cls, app):
        @app.route('/images/')
        def send_image():
            name = request.args.get('name', None)
            if name is None:
                return None
            return send_from_directory(cls.get_config().image_folder(), name)

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

        @app.route('/thumbnails/<image_id>')
        def thumbnail(image_id):
            thumbnail_path = Thumbnailer.get_thumbnail(image_id, cls.get_config().image_folder())
            return send_file(thumbnail_path, mimetype='image/jpg')
