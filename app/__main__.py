if __name__ == '__main__':
    from app.main import app
    debug = True
    # FIXME: threaded=False is a workaround for SQLAlchemy problems with sessions in multiple
    # threads
    app.run(debug=debug, host='0.0.0.0', port=5000, threaded=False)
