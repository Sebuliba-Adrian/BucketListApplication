class Bucket(object):
    def __init__(self, title):
        self.title = title
        self.goals = {}

    def get_goals(self):
        return self.goals

    def add_goal(self, item):
        self.goals[goal.name] = goal
