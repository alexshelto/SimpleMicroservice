from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager

from main import app
from main import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
