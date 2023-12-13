from flask import (Flask,
                   request)
from flask_restful import Resource
import json

skills = [
    {
        'skill_id': 0,
        'skill': 'Python'
    },
    {
        'skill_id': 1,
        'skill': 'Django'
    },
    {
        'skill_id': 2,
        'skill': 'Flask'
    }
]


class Skills(Resource):

    def get(self, skill_id):
        try:
            response = skills[skill_id]
        except IndexError:
            message = 'Developer id {} does not exist'.format(skill_id)
            response = {'status': 'fail', 'message': message}

        except Exception:
            message = 'Unknown error. Contact API Administrator '
            response = {'status': 'fail', 'message': message}

        return response

    def put(self, skill_id):
        data = json.loads(request.data)
        skills[skill_id] = data
        return data

    def delete(self, skill_id):
        skills.pop(skill_id)
        return {'status': 'success', 'message': 'register deleted'}


class SkillList(Resource):

    def post(self):
        data = json.loads(request.data)
        position = len(skills)
        data['dev_id'] = position
        skills.append(data)

        return skills[position]

    def get(self):
        return skills
