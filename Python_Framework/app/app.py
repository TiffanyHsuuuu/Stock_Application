import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask import render_template

from security import authenticate, identity
from resources.user_controller import UserController
from resources.stock_controller import StockController, StockList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(UserController, '/register')
api.add_resource(StockController, '/stock/<string:name>')
api.add_resource(StockList, '/stocks')

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def frontpage():
    return render_template('frontpage.html')


@app.route('/stockdetails')
def stockdetails():
    return render_template('stockdetails.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
