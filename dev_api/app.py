from flask import (Flask,
                   jsonify,
                   request
                   )
import json

app = Flask(__name__)

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

#  Return a developer by ID, it also updates and delete a developer
@app.route('/dev/<int:dev_id>/', methods=['GET', 'PUT', 'DELETE'])
def developer(dev_id):
    if request.method == 'GET':
        try:
            response = developers[dev_id]
        except IndexError:
            message = 'Developer id {} does not exist'.format(dev_id)
            response = {'status': 'fail', 'message': message}

        except Exception:
            message = 'Unknown error. Contact API Administrator '
            response = {'status': 'fail', 'message': message}

        return jsonify(response)

    elif request.method == 'PUT':
        data = json.loads(request.data)
        developers[dev_id] = data
        return jsonify(data)

    elif request.method == 'DELETE':
        developers.pop(dev_id)
        return jsonify({'status': 'success', 'message': 'register deleted'})


#  Returns all developers and allows to add a new one
@app.route('/dev/', methods=['POST', 'GET'])
def lists_developers():
    if request.method == 'POST':
        data = json.loads(request.data)
        position = len(developers)
        data['dev_id'] = position
        developers.append(data)

        return jsonify(developers[position])

    elif request.method == 'GET':
        return jsonify(developers)

if __name__ == '__main__':
    app.run(debug=True)
