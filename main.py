import json

from flask import Flask, request, jsonify, make_response
from flask_expects_json import expects_json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from jsonschema import ValidationError
from datetime import datetime

from model import ProductModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@postgres:5432/postgres"
app.config["REDIS_URL"] = "redis://:febriano@redis:6379/0"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
redis_client = FlaskRedis(app)


schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'price': {'type': 'integer'},
        'quantity': {'type': 'integer'},
    },
    'required': ['name', 'description', 'price', 'quantity']
}


@app.route("/product", methods=["GET", "POST"])
@expects_json(schema, ignore_for=["GET"])
def product():
    if request.method == 'GET':

        if redis_client.keys('product'):
            print("Fetch data from redis")
            result = json.loads(redis_client.get('product'))
        else:
            print("Fetch data from database")
            products = ProductModel.query.all()
            result = [
                {
                    "product_id": product.product_id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "quantity": product.quantity,
                    "created_date": str(product.created_date)
                }
            for product in products]

            redis_client.set('product', json.dumps(result), ex=900)

        # sorting data menggunakan fungsi python
        if request.values.get('sort') == 'date' and request.values.get('reverse'):
            data = sorted(result, key=lambda d: d['created_date'], reverse=True if request.values.get('reverse') == 'true' else False)
        elif request.values.get('sort') == 'price' and request.values.get('reverse'):
            data = sorted(result, key=lambda d: d['price'], reverse=True if request.values.get('reverse') == 'true' else False)
        elif request.values.get('sort') == 'name' and request.values.get('reverse'):
            data = sorted(result, key=lambda d: d['name'], reverse=True if request.values.get('reverse') == 'true' else False)
        else:
            data = result

        return jsonify(
            message='success',
            status_code=200,
            data=data
        )

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_product = ProductModel(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                quantity=data['quantity'],
                created_date=datetime.now()
            )
            db.session.add(new_product)
            db.session.commit()

            redis_client.delete('product')

            return jsonify(
                message='success',
                status_code=201
            ), 201
        else:
            return jsonify(
                message='Bad Request',
                status_code=400,
            )


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    # handle other "Bad Request"-errors
    return error
