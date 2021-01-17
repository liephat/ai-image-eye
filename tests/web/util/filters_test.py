from app.web.util.filters import escape_url, unescape_url


def test_escape_url():
    assert escape_url('asdf') == 'asdf'
    assert escape_url('asdf/qwer&xyz\\blah') == 'asdf%2Fqwer%26xyz%5Cblah'


def test_unescape_url():
    assert unescape_url('asdf') == 'asdf'
    assert unescape_url('asdf%2Fqwer%26xyz%5Cblah') == 'asdf/qwer&xyz\\blah'
