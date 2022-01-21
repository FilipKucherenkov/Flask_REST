import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required = True, help='Field cannot be left blank')
    parser.add_argument('name', type=str, required = False, help='Field cannot be left blank')
    
    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_item_by_name(name)
        except:
            return {'message': 'An error occured while searching for the item.'}, 500

        if item:
            return item.json()
        else:
            return {'message': 'There is no item with such name.'}, 404
    
    def post(self, name):
        request_data = self.parser.parse_args()

        item = ItemModel.find_item_by_name(name)
        if item:
            return {'message': 'There is an item with the same name.'}, 404

        item = ItemModel(name,request_data['price'])
        try:
            item.insert()
        except:
            return {'message': 'An error occured while inserting the item.'}, 500

        return item.json(), 201

    def delete(self, name):
        try:
            item = ItemModel.find_item_by_name(name)
        except:
            return {'message': 'An error occured while searching for the item.'}, 500

        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()

            return {'message': 'item has been deleted successfully'}, 201
        else:
            return {'message': 'There isn\'t an item with that name'}, 404
        
    def put(self, name):
        try:
            item = ItemModel.find_item_by_name(name)
        except:
            return {'message': 'An error occured while searching for the item.'}, 500

        if not item:
            return {'message': 'There isn\'t an item with the same name.'}, 404

        request_data = self.parser.parse_args()
        updated_item = ItemModel(name, request_data['price'])
        updated_item.update(request_data['name'])
        
        return {'message':'Item has been updated'}, 201


class ItemList(Resource):

     def get(self):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "SELECT * FROM items"
            result = cursor.execute(query)
            items = result.fetchall()
            connection.close()
            return {'items': items}, 201
