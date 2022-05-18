from dataclasses import dataclass

import requests
from flask import abort
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from producer import publish
from sqlalchemy import UniqueConstraint

app = Flask(__name__)

# sql://user:pwd@host(db from docker)/name from docker file
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main_db'
CORS(app)  # Frontend will need CORS


db = SQLAlchemy(app)

migrate = Migrate(app, db)


# Product created in Django App (ADMIN)
# This model will catch the event from rabbitMQ and create the product
@dataclass  # Allows to be jsonified
class Product(db.Model):
    pk: int
    title: str
    image: str
    pk = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    # Makes sure combo of user_id and product_id are unique
    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    print(Product.query.all())
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    print('Request for like on product with id: ', id)
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()

    print('Still in like')

    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
        print('Event sent to admin')
        # Send event

    except:
        abort(400, 'you already liked this product')
        print('Had to abort like for some reason')

    return jsonify({
        'message': 'success'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
