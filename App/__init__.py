from flask import Flask

from App import settings
from App.apis import init_api
from App.ext import init_ext


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.envs.get("develop"))

    init_ext(app)
    init_api(app)

    return app
