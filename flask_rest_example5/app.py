from flask import Flask
from security import authenticate, identity
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


from db import db

#Create initial flask app.
app = Flask(__name__)

#DB configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # can be any db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # use SQLAlchemy's way of tracking modifications.

app.secret_key = "2201"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

#Resources 
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

#This only runs if this file is being run initially
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)