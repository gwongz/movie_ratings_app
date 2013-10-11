try:
    import judgement
except ImportError:
    raise SystemExit('Could not find judgement.py. Does it exist?')


import unittest
import os
import tempfile
import flask
from flask import request, jsonify, Flask
from mock import Mock 
import model
import json
from mock import patch

class JudgementTestCase(unittest.TestCase):
	def setUp(self):
		self.db_fd, judgement.app.config['DATABASE'] = tempfile.mkstemp()
		judgement.app.config['TESTING'] = True
		self.app = judgement.app.test_client()
		model.init_db()
	
	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(judgement.app.config['DATABASE'])

	# helper functions 
	def login(self, username, password):
		return self.app.post('/login', data=dict(
			username=username,
			password=password
			), follow_redirects=True)
	
	def logout(self):
		return self.app.get('/logout', follow_redirects=True)


	def create_unique_user(self, email, password, age, gender, occupation, zipcode):
		return self.app.post('/create_user', data=dict(
			email=email,
			password=password,
			age=age,
			gender=gender,
			occupation=occupation,
			zipcode=zipcode), follow_redirects=True)

	# test functions
	def test_login_logout(self):
		response = self.login('abc123', 'def123')
		assert "You were successfully logged in" in response.data
		response = self.logout()
		assert "You have been logged out" in response.data 
		response = self.login('grace', 'hackbright')
		assert 'Invalid credentials' in response.data 


	def test_urls(self):
		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/index', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/login', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/search', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/user', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/all_movies', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/logout', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/nonexistent', follow_redirects=True)
		assert "Page Not Found" in response.data
		self.assertEqual(response.status_code, 404)	


	def test_create_unique_user(self):
		existing_user = model.User.query.filter(model.User.email=='abc123').one()
		existing_user_password = existing_user.password 
		response = self.create_unique_user('abc123', 'hello', 30, "female", "student", 94109)
		self.assertFalse(existing_user_password=='hello')
		assert "That email is already taken." in response.data
		print response.data


if __name__=="__main__":
	unittest.main()