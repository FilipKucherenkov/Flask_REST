from flask import Flask
from security import authenticate, identity
from flask_restful import Api
from flask_jwt import JWT
from appUser import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = "2201"
api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
app.run(port=5000, debug=True)