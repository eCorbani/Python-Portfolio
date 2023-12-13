import json
from flask import (Flask,
                   request)
from flask_restful import (Resource,
                           Api)
from flask_httpauth import HTTPBasicAuth

from models import (People,
                    Tasks,
                    Users)

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

''''
  Simple example
USERS = {
    'edson': '111',
    'corbani': '321'
}

@auth.verify_password
def verification(login, password):
    if not (login, password):
        return False
    return USERS.get(login) == password
'''


@auth.verify_password
def verification(login, password):
    if not (login, password):
        return False
    return Users.query.filter_by(login=login, password=password, active=True).first()


class Person(Resource):
    def get(self, name):
        person = People.query.filter_by(name=name).first()
        try:
            response = {
                'name': person.name,
                'age': person.age,
                'id': person.id
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'register not found'
            }

        return response

    @auth.login_required
    def put(self, name):
        person = People.query.filter_by(name=name).first()
        data = json.loads(request.data)

        try:
            if 'name' in data:
                person.name = data['name']

            if 'age' in data:
                person.age = data['age']

            person.save()

            response = {
                'id': person.id,
                'name': person.name,
                'age': person.age
            }

        except AttributeError:
            response = {
                'status': 'error',
                'message': 'register not found'
            }

        return response

    @auth.login_required
    def delete(self, name):
        person = People.query.filter_by(name=name).first()
        try:
            person.delete()
            message = f'Person {person.name} removed with success'

            response = {'status': 'success', 'message': message}
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'register not found'
            }

        return response


class PeopleList(Resource):
    def get(self):
        people = People.query.all()
        try:
            response = [{'id': i.id, 'name': i.name, 'age': i.age} for i in people]

        except AttributeError:
            response = {
                'status': 'error',
                'message': 'register not found'
            }
        return response

    @auth.login_required
    def post(self):
        data = json.loads(request.data)
        person = People(name=data['name'], age=data['age'])

        response = {
            'id': person.id,
            'name': person.name,
            'age': person.age
        }

        person.save()

        return response


class Task(Resource):
    def get(self, person):
        tasks = Tasks.query.join(People).filter(People.name == person).all()

        if tasks:
            response = [{'owner': i.person.name, 'id': i.id, 'name': i.name} for i in tasks]

        else:
            response = {
                'status': 'error',
                'message': 'register not found'
            }

        return response


class TaskList(Resource):

    def get(self):
        tasks = Tasks.query.all()

        if tasks:
            response = [{'owner': i.person.name, 'status': i.status, 'id': i.id, 'name': i.name} for i in tasks]

        else:
            response = {
                'status': 'error',
                'message': 'register not found'
            }

        return response

    @auth.login_required
    def post(self):
        data = json.loads(request.data)
        person = People.query.filter_by(name=data['person']).first()
        task = Tasks(name=data['name'], person=person, status=data['status'])

        response = {
            'id': task.id,
            'person': task.person.name,
            'name': task.name,
            'status': task.status
        }

        task.save()

        return response


class TaskStatus(Resource):

    def get(self, id):
        task = Tasks.query.filter_by(id=id).first()
        try:
            response = {
                'id': task.id,
                'name': task.name,
                'owner': task.person.name,
                'status': task.status
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'register not found'
            }

        return response

    @auth.login_required
    def put(self, id):

        task = Tasks.query.filter_by(id=id).first()
        data = json.loads(request.data)

        try:
            if 'status' in data:
                task.status = data['status']

                task.save()

                response = {
                    'id': task.id,
                    'owner': task.person.name,
                    'name': task.name,
                    'status': task.status
                }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'register not found'
            }

        return response


api.add_resource(Person, '/person/<string:name>/')
api.add_resource(PeopleList, '/person/')
api.add_resource(Task, '/tasks/<string:person>')
api.add_resource(TaskList, '/tasks/')
api.add_resource(TaskStatus, '/tasks/status/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
