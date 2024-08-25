#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, RestaurantPizza, Pizza
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants")
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify({"restaurants": [restaurant.to_dict() for restaurant in restaurants]})

@app.route("/restaurants/<int:id>")
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.to_dict())
    return jsonify({"error": "Restaurant not found"}), 404

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return "", 204
    return jsonify({"error": "Restaurant not found"}), 404

@app.route("/pizzas")
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify({"pizzas": [pizza.to_dict() for pizza in pizzas]})

@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.json
    try:
        restaurant_pizza = RestaurantPizza(
            price=data["price"],
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"]
        )
        db.session.add(restaurant_pizza)
        db.session.commit()
        return jsonify(restaurant_pizza.to_dict()), 201
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)
