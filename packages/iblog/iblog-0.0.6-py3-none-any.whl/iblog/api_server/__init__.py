from .api import blueprint


class ApiServer(object):
    def __init__(self, host='0.0.0.0', port=8080, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        from flask import Flask
        app = Flask(__name__)
        app.register_blueprint(blueprint, url_prefix='/api')
        self.app = app

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)
