from flask import Flask, jsonify, abort, make_response, request,request, session, g, redirect, url_for, abort,render_template, flash, _app_ctx_stack

from models.user import User


NOT_FOUND = 'Not found'
BAD_REQUEST = 'Bad request'

app = Flask(__name__)

users_datastore = {}

goals = [
    {
        'id': 1,
        'name': 'Board a bullet train',
        'status': 1
    },
    {
        'id': 2,
        'name': 'Climb mountain Kirimanjaro',
        'status': 0,
    },
    {
        'id': 3,
        'name': 'Go sky diving',
        'status': 1,
    }
]


def _get_goal(id):
    return [goal for goal in goals if goal['id'] == id]


def _record_exists(name):
    return [goal for goal in goals if goal["name"] == name]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': NOT_FOUND}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': BAD_REQUEST}), 400)


@app.route('/bucketlist/v1.0/register', methods=['GET', 'POST'])
def register_user():
    """A function to register  a user"""
    if request.method == 'POST':
        if request.form['password'] == request['repeat_pass']:
            users_datastore[request.form['username']] = User(
                request.form['name'], request.form['username'], request.form['password'])
            return redirect('/index')
        else:
            return 'Password missmatch please try again'
    else:

        return render_template('registration.html')


@app.route('/bucketlist/v1.0/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        if request.form['username'] in users_datastore:
            if request.form['password'] == users_datastore[request.form['username']].password:
                session['active_user'] = request.form['username']
                return redirect('/main')
            else:
                return redirect('/index')
        else:
            return redirect('/registration')
    else:
        return render_template('index.html')


@app.route('/bucketlist/v1.0/goals', methods=['GET'])
def get_goals():
    return jsonify({'goals': goals})


@app.route('/bucketlist/v1.0/goals/<int:id>', methods=['GET'])
def get_goal(id):
    goal = _get_goal(id)
    if not goal:
        abort(404)
    return jsonify({'goals': goal})


@app.route('/bucketlist/v1.0/goals', methods=['POST'])
def create_goal():
    if not request.json or 'name' not in request.json or 'status' not in request.json:
        abort(400)
    goal_id = goals[-1].get("id") + 1
    name = request.json.get('name')
    if _record_exists(name):
        abort(400)
    status = request.json.get('status')
    if type(status) is not int:
        abort(400)
    goal = {"id": goal_id, "name": name,
            "status": status}
    goals.append(goal)
    return jsonify({'goal': goal}), 201


@app.route('/bucketlist/v1.0/goals/<int:id>', methods=['PUT'])
def update_goal(id):
    goal = _get_goal(id)
    if len(goal) == 0:
        abort(404)
    if not request.json:
        abort(400)
    name = request.json.get('name', goal[0]['name'])
    status = request.json.get('status', goal[0]['status'])
    if type(status) is not int:
        abort(400)
    goal[0]['name'] = name
    goal[0]['status'] = status
    return jsonify({'goal': goal[0]}), 200


@app.route('/bucketlist/v1.0/goals/<int:id>', methods=['DELETE'])
def delete_goal(id):
    goal = _get_goal(id)
    if len(goal) == 0:
        abort(404)
    goals.remove(goal[0])
    return jsonify({}), 204


if __name__ == '__main__':
    app.run(debug=True)
