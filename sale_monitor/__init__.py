import os
from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Attempting to allow the React app to hit these APIs on the dev port
    # CORS at a high level to even make requests to the server
    # and supports_credentials so that we can submit the cookies
    CORS(app, supports_credentials=True)

    print(f'This is the flask_env: {os.getenv("FLASK_ENV")}')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'sale_monitor.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from sale_monitor.database import db
    db.init_app(app)

    from .endpoints.settings import search_stores, set_email, set_store
    app.register_blueprint(search_stores.bp)
    app.register_blueprint(set_email.bp)
    app.register_blueprint(set_store.bp)

    from .endpoints.watched_items import delete_watched, new_watched, update_watched
    app.register_blueprint(delete_watched.bp)
    app.register_blueprint(new_watched.bp)
    app.register_blueprint(update_watched.bp)

    from .endpoints.initialization import has_session, start_session
    app.register_blueprint(has_session.bp)
    app.register_blueprint(start_session.bp)

    from .endpoints import search_products
    from sale_monitor.endpoints.initialization import get_all
    app.register_blueprint(get_all.bp)
    app.register_blueprint(search_products.bp)

    return app