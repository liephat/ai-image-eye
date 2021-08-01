import os

if __name__ == '__main__':
    from app.main import app

    os.environ['FLASK_DEBUG'] = '1'

    app.run(host='0.0.0.0', port=5000, threaded=True)
