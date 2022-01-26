from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):


    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if(store):
            return store, 201
        else:
            return {'message': 'There is no store with that name.'}, 401

    def put(self, name):
        store = StoreModel.find_store_by_name(name)
        if(store):
            return {'message': 'Store with that name already exists.'}, 401
        
        newStore = StoreModel(name)
        newStore.save_to_db()

        return newStore.json()

    def delete(self, name):
        store = StoreModel.find_store_by_name(name)
        if(store):
            store.delete_from_db()
            return {'message': 'Store succefully deleted'}, 404
        else:
            return {'message': 'There is no store with that name.'}, 401

class StoreList(Resource):

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}, 201