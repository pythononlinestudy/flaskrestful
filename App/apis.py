from flask import request
from flask_restful import Api, Resource, fields, marshal_with, reqparse

from App.ext import db
from App.models import Cat

api = Api()


def init_api(app):
    api.init_app(app=app)

"""
{
    "status":"200",
    "msg": "ok",
    "data": [
        {
            "c_name": "XX",
            "c_age"： “1”，
            “id”： “2”
        },
        {
            "c_name": "XX",
            "c_age"： “1”，
            “id”： “2”
        },
    ]
}

"""
cat_fields = {
    "c_name": fields.String,
    "c_age": fields.Integer,
    # "id": fields.Integer
    "c_id": fields.Integer
}

cat_result_fields = {
    "status": fields.String,
    "msg": fields.String,
    "data": fields.Nested(cat_fields)
}

cat_resource_fields = {
    "status": fields.String,
    "msg": fields.String,
    "data": fields.List(fields.Nested(cat_fields))
}


parser = reqparse.RequestParser()
parser.add_argument("c_name", type=str)
parser.add_argument("c_age", type=int)

parser_del = parser.copy()
parser_del.add_argument("id", type=int, required=True, help="删除必须提供id")

parser_patch = parser_del.copy()
parser_patch.remove_argument("id")
parser_patch.add_argument("id", type=int, required=True, help= "信息修改必须提供id")


class CatResource(Resource):

    @marshal_with(cat_resource_fields)
    def get(self):

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 2))

        cats = Cat.query.offset((per_page*(page-1))).limit(per_page)
        return {"msg": "ok", "status": "200", "data": cats}

    @marshal_with(cat_result_fields)
    def post(self):
        parse = parser.parse_args()
        name = parse.get("c_name")
        age = parse.get("c_age")
        cat = Cat()
        cat.c_name = name
        cat.c_age = age

        db.session.add(cat)
        db.session.commit()

        return {"msg": "ok", "data": cat}, 201

    def delete(self):
        parse = parser_del.parse_args()
        id = parse.get("id")
        cat = Cat.query.get(id)
        data = {
            "status": "204"
        }
        if cat:
            db.session.delete(cat)
            db.session.commit()
            data["msg"] = "delete success"
        else:
            data["msg"] = "does not exist"
        return data

    @marshal_with(cat_result_fields)
    def patch(self):
        parse = parser_patch.parse_args()
        id = parse.get("id")
        name = parse.get("c_name")
        age = parse.get("c_age")

        cat = Cat.query.get(id)

        if not cat:
            return {"msg": "指定猫咪不存在"}

        if name:
            cat.c_name = name
        if age:
            cat.c_age = age

        db.session.add(cat)
        db.session.commit()

        return {"msg": "ok", "status": "201", "data": cat}


api.add_resource(CatResource, "/cats/")


