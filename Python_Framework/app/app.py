import os
import pandas as pd
from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

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

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def frontpage():
    return render_template('frontpage.html')


@app.route('/stockdetails')
def stockdetails():
    df = pd.read_csv('AAPL_data.csv', sep=r'\t', engine='python')
    labels = df['date'].values
    values = df['4. close'].values
    return render_template('stockdetails.html', values=values, labels=labels)

@app.route('/predictions')
def predictions():
    df = pd.read_csv('AAPL_data.csv', sep=r'\t', engine='python')
    labels = df['date'].values
    predictions = pd.read_csv('predictions.csv', sep=',')
    targets = pd.read_csv('targets.csv', sep=',')
    return render_template('predictions.html',labels=labels, predictions=predictions, targets=targets)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
