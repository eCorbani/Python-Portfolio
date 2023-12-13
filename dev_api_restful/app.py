from flask import (Flask,
                   request)
from flask_restful import (Resource,
                           Api)
from skills import Skills
from skills import SkillList

import json

app = Flask(__name__)
api = Api(app)

developers = [
    {
        'dev_id': 0,
        'name': 'Edson',
        'skills': ['Python', 'Flask']
    },
    {
        'dev_id': 1,
        'name': 'Nádia',
        'skills': ['Invisalign', 'DJango']
    },
    {
        'dev_id': 2,
        'name': 'Léo',
        'skills': ['DJ', 'Storyteller']
    },
]


class Developers(Resource):

    def get(self, dev_id):
        try:
            response = developers[dev_id]
        except IndexError:
            message = 'Developer id {} does not exist'.format(dev_id)
            response = {'status': 'fail', 'message': message}

        except Exception:
            message = 'Unknown error. Contact API Administrator '
            response = {'status': 'fail', 'message': message}

        return response

    def put(self, dev_id):
        data = json.loads(request.data)
        developers[dev_id] = data
        return data

    def delete(self, dev_id):
        developers.pop(dev_id)
        return {'status': 'success', 'message': 'register deleted'}


class DeveloperList(Resource):

    def post(self):
        data = json.loads(request.data)
        position = len(developers)
        data['dev_id'] = position
        developers.append(data)

        return developers[position]

    def get(self):
        return developers


api.add_resource(Developers, '/dev/<int:dev_id>/')
api.add_resource(DeveloperList, '/dev/')

api.add_resource(Skills, '/skills/<int:skill_id>/')
api.add_resource(SkillList, '/skills/')

if __name__ == '__main__':
    app.run(debug=True)
