try:
    import judgement
except ImportError:
    raise SystemExit('Could not find judgement.py. Does it exist?')

import unittest
import os
import tempfile
import flask
from flask import request, jsonify, Flask
import mock
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
				
	def test_movie(self):
		with self.app as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1
			response = self.app.get('/movie/1', follow_redirects=True)
			self.assertEqual(response.status_code, 200)
			assert "Toy Story" in response.data
			assert "Your rating" in response.data	

	# checking validity of sign up form
	def test_create_unique_user(self):
		existing_user = model.User.query.filter(model.User.email=='admin').one()
		existing_user_password = existing_user.password 
		response = self.create_unique_user('admin', 'hello', 30, "female", "student", 94109)
		self.assertFalse(existing_user_password=='hello')
		assert "That email is already taken." in response.data
		# need to add condition for empty sign up form and incomplete form

	def change_rating(self, movie_id, value):
		return self.app.post('/rating', data=dict(
						movie_id=movie_id, rating=rating), follow_redirects=True)

	def test_change_rating_in_db(self):
		# fake session with user 1 
		with self.app as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1
			existing_rating = model.Rating.query.filter(model.Rating.movie_id==1).filter(model.Rating.user_id==1).one()	
			#set existing rating to 1
			existing_rating.rating=1
			# change the rating to 5
			response = self.app.post('/rating', data=dict(movie_id=1, rating=5), follow_redirects=True)
			assert "Your rating has been updated" in response.data
			updated_rating = model.Rating.query.filter(model.Rating.movie_id==1).filter(model.Rating.user_id==1).one()
			self.assertTrue(existing_rating != updated_rating)

if __name__=="__main__":
	unittest.main()