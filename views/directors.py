from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        data = request.json
        return director_service.create(data), 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    def put(self, rid):
        data = request.json
        if not data.get('id') or (data.get('id') != rid):
            data['id'] = rid

        return director_service.update(data), 200

    def delete(self, rid):
        return director_service.delete(rid), 200
