import urllib


def escape_url(text):
    """ Encode reserved URL characters to their '%..' representation
    E.g. / becomes %2F
    """
    return urllib.parse.quote(text, safe='')


def unescape_url(text):
    """ Decode reserved URL characters from their '%..' representation """
    return urllib.parse.unquote(text)


def init_filters(app):
    # pylint: disable=unused-variable
    @app.template_filter()
    def url_escape(text):
        return escape_url(text)
