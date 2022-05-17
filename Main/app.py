from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)

# sql://user:pwd@host(db from docker)/name from docker file
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main_db'
CORS(app)  # Frontend will need CORS


db = SQLAlchemy(app)

migrate = Migrate(app, db)


# Product created in Django App (ADMIN)
# This model will catch the event from rabbitMQ and create the product
class Product(db.Model):
    pk = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


class ProductUser(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    # Makes sure combo of user_id and product_id are unique
    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')