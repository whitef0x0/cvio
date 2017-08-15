from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, migrate, upgrade
from sqlalchemy_utils import database_exists, create_database

from application.app import app, db
from gunicorn_script import GunicornServer

_migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)
manager.add_command('rungunicorn', GunicornServer())

@manager.command
def create_db():
	"""Creates the db tables."""
	with app.app_context():
		print("Loaded Flask App Context\n")
		if not database_exists(db.engine.url): 
			create_database(db.engine.url)
			print("Created Database\n")
		db.create_all()

@manager.command
def setup_db():
	"""Creates the db tables."""
	with app.app_context():
		print("Loaded Flask App Context\n")
		if not database_exists(db.engine.url): 
			create_database(db.engine.url)
			print("Created Database\n")
			db.create_all()
		upgrade()
		migrate()
		print("Successfully Performed Migrations\n")

if __name__ == '__main__':
	manager.run()
