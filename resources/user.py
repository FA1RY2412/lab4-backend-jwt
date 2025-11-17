from flask_restful import Resource, reqparse
from models.user import UserModel
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

user_parser = reqparse.RequestParser()
user_parser.add_argument("username", type=str, required=True)
user_parser.add_argument("password", type=str, required=True)

class UserRegister(Resource):
    def post(self):
        data = user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "User exists"}, 400

        user = UserModel(username=data["username"],
                         password=pbkdf2_sha256.hash(data["password"]))
        user.save_to_db()

        return {"message": "Registered"}, 201

class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        if user and pbkdf2_sha256.verify(data["password"], user.password):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200

        return {"message": "Invalid credentials"}, 401

