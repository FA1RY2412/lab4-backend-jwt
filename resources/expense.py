from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.expense import ExpenseModel

parser = reqparse.RequestParser()
parser.add_argument("title", type=str)
parser.add_argument("amount", type=float)

class ExpenseList(Resource):
    @jwt_required()
    def get(self):
        return {"expenses": [e.json() for e in ExpenseModel.query.all()]}

    @jwt_required()
    def post(self):
        data = parser.parse_args()
        exp = ExpenseModel(**data)
        exp.save_to_db()
        return exp.json(), 201

class ExpenseSingle(Resource):
    @jwt_required()
    def get(self, id):
        e = ExpenseModel.find(id)
        if e:
            return e.json()
        return {"message": "Not found"}, 404
