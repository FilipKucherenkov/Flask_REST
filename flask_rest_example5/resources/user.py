import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str , required = True)
    parser.add_argument('password', type=str , required = True)


    def post(self):
        request_data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(request_data['username']):
            return {'message':'This username has already been taken'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query,(request_data['username'], request_data['password'],))

        connection.commit()
        connection.close()

        return {'message':'the user was created successfully'}, 201
        
