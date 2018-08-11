from flask import Flask
from flask import render_template

from backend.controller.driver_controller import driver_controller
from std import config
from std.network import api
from std.log import log
from backend.controller.app_controller import app_controller
from backend.controller.build_controller import build_controller


app = Flask(__name__,
            template_folder=config.TEMPLATE_PATH,
            static_folder=config.STATIC_PATH)
app.register_blueprint(app_controller)
app.register_blueprint(build_controller)
app.register_blueprint(driver_controller)


# Variables for app.config
TMP_PATH = "TMP_PATH"
MAX_CONTENT_LENGTH = "MAX_CONTENT_LENGTH"

# Variables for image resources
app.config[TMP_PATH] = config.TEMP_PATH
app.config[MAX_CONTENT_LENGTH] = config.MAX_SIZE_FILE


@app.route(api.get_home)
@app.route(api.get_index)
def get_home():
    return render_template("index.html")


if config.IS_DEBUG:
    @app.after_request
    def add_header(session):
        session.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        session.headers["Pragma"] = "no-cache"
        session.headers["Expires"] = "0"
        session.headers['Cache-Control'] = 'public, max-age=0'
        return session


if __name__ == '__main__':
    if config.IS_DEBUG:
        log.configure_debug(config.LOGGING_MASK)
    else:
        log.configure_release(config.LOGGING_MASK, config.LOGGING_FILE)

    app.run(host=config.HOST)
