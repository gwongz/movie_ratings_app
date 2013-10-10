try:
    import judgement
except ImportError:
    raise SystemExit('Could not find judgement.py. Does it exist?')


import unittest
import os
import tempfile
from flask import request
import model

class JudgementTestCase(unittest.TestCase):
	def setUp(self):
		self.db_fd, judgement.app.config['DATABASE'] = tempfile.mkstemp()
		judgement.app.config['TESTING'] = True
		self.app = judgement.app.test_client()
		model.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(judgement.app.config['DATABASE'])

	def hello_username(self, username):
		return self.app.post('/hello', data={'username':username})

	def test_hello_username(self):
		expected = "Hello nobody"
		response = self.app.get('/hello')
		assert expected in response.data

	def login(self, username, password):
		return self.app.post('/login', data=dict(
			username=username,
			password=password
			), follow_redirects=True)
	
	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def test_login_logout(self):
		expected = "You were successfully logged in"
		response = self.app.post('/login', data=dict(
			username='abc123', 
			password='def123'), follow_redirects = True)
		assert expected in response.data

		


if __name__=="__main__":
	unittest.main()