from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required = True, help='Field cannot be left blank')
    parser.add_argument('name', type=str, required = False, help='Field cannot be left blank')
    parser.add_argument('store_id', type=int, required = False, help='Field cannot be left blank')

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

        item = ItemModel(name,request_data['price'], request_data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured while inserting the item.'}, 500

        return item.json(), 201

    def delete(self, name): 
        item = ItemModel.find_item_by_name(name)
      
        if item:
            item.delete_from_db()
            return {'message': 'item has been deleted successfully'}, 201
        else:
            return {'message': 'There isn\'t an item with that name'}, 404
        
    def put(self, name):
        request_data = self.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        

        if not item:
            item = ItemModel(name, request_data['price'], request_data['store_id'])
            # return {'message': 'There isn\'t an item with the same name.'}, 404
        else:
            item.price = request_data['price']
            item.store_id = request_data['store_id']
        
        item.save_to_db() 
        return item.json(), 201


class ItemList(Resource):

     def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 201
