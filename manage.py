from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand, migrate, upgrade
from sqlalchemy_utils import database_exists, create_database

from application.app import app, db
from gunicorn_script import GunicornServer

_migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("runprodserver", Server(
        use_debugger = False,
            use_reloader = False,
                host = '0.0.0.0',
                port = 5000) )

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
