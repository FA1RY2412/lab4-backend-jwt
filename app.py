import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.user import UserRegister, UserLogin
from resources.expense import ExpenseList, ExpenseSingle

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["JWT_SECRET_KEY"] = "5277283bc6313e176aa6d973c97956d2d95cdff30f5840f20de916225a03ad38"

    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired(jwt_header, jwt_payload):
        return jsonify({"message": "Token expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid(error):
        return jsonify({"message": error, "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing(error):
        return jsonify({"message": "Missing token", "error": "authorization_required"}), 401

    api.add_resource(UserRegister, "/register")
    api.add_resource(UserLogin, "/login")
    api.add_resource(ExpenseList, "/expenses")
    api.add_resource(ExpenseSingle, "/expense/<int:id>")

    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
