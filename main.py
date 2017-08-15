from flask_migrate import Migrate, migrate, upgrade
from sqlalchemy_utils import database_exists, create_database
from application.app import app, db

def application_start():
	with app.app_context():
		print("Loaded Flask App Context\n")
		if not database_exists(db.engine.url): 
		    create_database(db.engine.url)
		    print("Created Database\n")
		_migrate = Migrate(app, db)
		upgrade()
		migrate()
		print("Successfully Performed Migrations\n")
