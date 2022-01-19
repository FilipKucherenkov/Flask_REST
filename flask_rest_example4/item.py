
from multiprocessing import connection
import re
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required = True, help='Field cannot be left blank')
    parser.add_argument('name', type=str, required = False, help='Field cannot be left blank')
    
    def find_item_by_name(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        item = result.fetchone()
        connection.close()

        if item:
            return item
        else:
            return None
    
    @jwt_required()
    def get(self, name):
        item = self.find_item_by_name(name)

        if item:
            return {'item': {'name': item[0], 'price':item[1]}}
        else:
            return {'message': 'There is no item with such name.'}, 404
    
    def post(self, name):
        request_data = self.parser.parse_args()

        item = self.find_item_by_name(name)
        if item:
            return {'message': 'There is an item with the same name.'}, 404


        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        item = {'name': name, 'price': request_data['price']}

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

        return item, 201

    def delete(self, name):
        item = self.find_item_by_name(name)
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
        item = self.find_item_by_name(name)
        if not item:
            return {'message': 'There isn\'t an item with the same name.'}, 404

        request_data = self.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'UPDATE items SET name = ?, price = ? WHERE name=?'
        cursor.execute(query, (request_data['name'],request_data['price'], name ))
        connection.commit()
        connection.close()
        
        return {'message':'Item has been updated'}, 201

class ItemList(Resource):
     def get(self):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "SELECT * FROM items"
            result = cursor.execute(query)
            items = result.fetchall()
            return {'items': items}, 201
