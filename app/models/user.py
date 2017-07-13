class User(object):
	def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.buckets = {}

    def get_buckets(self):
        return self.buckets
