from copy import deepcopy
import unittest
import json

import app

BASE_URL = 'http://127.0.0.1:5000/bucketlist/v1.0/goals'
BAD_goal_URL = '{}/5'.format(BASE_URL)
GOOD_goal_URL = '{}/3'.format(BASE_URL)


class TestBucketListApp(unittest.TestCase):

    def setUp(self):
        self.backup_goals = deepcopy(app.goals)  # no references!
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_all(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['goals']), 3)

    def test_get_one(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['goals'][0]['name'], 'Board a bullet train')

    def test_goal_not_exist(self):
        response = self.app.get(BAD_goal_URL)
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        # missing status field = bad
        goal = {"name": "some_goal"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(goal),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # status field cannot take str
        goal = {"name": "goal", "status": 'string'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(goal),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # valid: both required fields, status takes int
        goal = {"name": "goal", "status": 200}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(goal),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['goal']['id'], 4)
        self.assertEqual(data['goal']['name'], 'goal')
        # cannot add goal with same name again
        goal = {"name": "goal", "status": 200}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(goal),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update(self):
        goal = {"status": 1 }
        response = self.app.put(GOOD_goal_URL,
                                data=json.dumps(goal),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['goal']['status'], 1)
        # proof need for deepcopy in setUp: update app.goals should not affect self.backup_goals
        # this fails when you use shallow copy
        self.assertEqual(self.backup_goals[2]['status'], 1)  # org status

    def test_update_error(self):
        # cannot edit non-existing goal
        goal = {"status": 30}
        response = self.app.put(BAD_goal_URL,
                                data=json.dumps(goal),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)
        # status field cannot take str
        goal = {"status": 'string'}
        response = self.app.put(GOOD_goal_URL,
                                data=json.dumps(goal),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        response = self.app.delete(GOOD_goal_URL)
        self.assertEqual(response.status_code, 204)
        response = self.app.delete(BAD_goal_URL)
        self.assertEqual(response.status_code, 404)

   
        

    def tearDown(self):
        # reset app.goals to initial state
        app.goals = self.backup_goals


if __name__ == "__main__":
    unittest.main()
