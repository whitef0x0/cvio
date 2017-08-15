from flask_script import Command, Option
from flask_migrate import Migrate, migrate, upgrade
from sqlalchemy_utils import database_exists, create_database

from application.app import app, db
import os, sys

class GunicornServer(Command):
    "Run the app within Gunicorn"
    def get_options(self):
        from gunicorn.config import make_settings
        settings = make_settings()
        options = []

        for setting, klass in settings.items():
            if klass.cli:
                options.append(Option(*klass.cli))
        return options

    def run(self, *args, **kwargs):

        #Migrate Database
        if not database_exists(db.engine.url): 
            create_database(db.engine.url)
        _migrate = Migrate(app, db)
        upgrade()
        migrate()

        from gunicorn.app.wsgiapp import WSGIApplication

        app = WSGIApplication()
        app.app_uri = 'manage:app'
        return app.run()