from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        data = request.json
        return genre_service.create(data), 201


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    def put(self, rid):
        data = request.json
        if not data.get('id') or (data.get('id') != rid):
            data['id'] = rid

        return genre_service.update(data), 200

    def delete(self, rid):
        return genre_service.delete(rid), 200
