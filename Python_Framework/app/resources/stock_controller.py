from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.stock import Stock

class StockController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('number',
                        type = int,
                        required = True,
                        help = 'This field cannot be blank!')
    parser.add_argument('price',
                        type = float,
                        required = True,
                        help = 'This field cannot be blank!')

    @jwt_required()
    def get(self, name):
        stock = Stock.find_by_name(name)
        if stock:
            return stock.json(), 200
        return {'message':'Stock not Found!'}, 404

    def post(self, name):
        if(Stock.find_by_name(name)):
            return {'message':'Stock already exists!'.format(name)}, 400

        data = StockController.parser.parse_args()
        stock = Stock(name, data['number'], data['price'])

        try:
            stock.save_to_db()
        except:
            return {'message':'Internal Error'}, 500
        return stock.json(), 201

    def delete(self, name):
        stock = Stock.find_by_name(name)
        if stock:
            stock.delete_from_db()
        return {'message':'Stock deleted!'}

    def put(self, name):
        data = StockController.parser.parse_args()
        stock = Stock.find_by_name(name)

        if stock:
            stock.number = data['number']
            stock.price = data['price']
        else:
            stock = Stock(name, data['numnber'], data['price'])

        stock.save_to_db()
        return stock.json()


class StockList(Resource):
    def get(self):
        return {'stocks': list(map(lambda x: x.json(), Stock.query.all()))}
