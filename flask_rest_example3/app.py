from flask import Flask, request
from security import authenticate, identity
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.secret_key = "2201"
api = Api(app)

jwt = JWT(app, authenticate, identity)


items = []

class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda item: item['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
    
    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            return {'message': "An item with name '{} already exists".format(name)}, 400

        request_data = request.get_json()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda item: item['name'] == name, items))
        return {'message': 'item has been deleted'}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required = True, help='Field cannot be left blank')
        request_data = parser.parse_args()

        for item in items:
            if item['name'] == name:
                item = {
                    'name': name,
                    'price': request_data['price']
                }
                items.append(item)
                return {'message': '{} has been updated'.format(name)}, 201
        return {'message':'item not found'}, 400

class ItemList(Resource):
     def get(self):
            return {'items': items}





api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)