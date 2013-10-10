try:
    import judgement
except ImportError:
    raise SystemExit('Could not find judgement.py. Does it exist?')


import unittest
import os
import tempfile
from flask import request, jsonify
import mock 
import model
import json

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

	def display_movie(self):
		return self.app.get('/movie?=<int:id>', follow_redirects=True)

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
	
	def test_display_movie(self):
		response = self.app.get('/movie?id=1')
		assert 'Toy Story' in response.data
	
	def test_urls(self):
		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/index', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/login', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/search', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/movie', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/user', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/all_movies', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		response = self.app.get('/logout', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_create_unique_user(self):
		existing_user = model.User.query.filter(model.User.email=='abc123').one()
		existing_user_password = existing_user.password 
		response = self.create_unique_user('abc123', 'hello', 30, "female", "student", 94109)
		self.assertFalse(existing_user_password=='hello')
		assert "That email is already taken." in response.data

	def test_change_rating(self):
		user = model.User.query.get(1)
		movie = model.Movie.query.get(1)
		rating_obj = model.Rating.query.filter(model.Rating.movie_id==1).filter(model.Rating.user_id==1).one()				
		rating = rating_obj.rating
		new_rating = 1
		rating_obj.rating = new_rating # updates existing record
		updated_obj = model.Rating.query.filter(model.Rating.movie_id==1).filter(model.Rating.user_id==1).one()
		updated_rating = updated_obj.rating 		
		self.assertEqual(updated_rating, new_rating)
		self.assertFalse(updated_rating==rating)
		 

	# def get csrf_request(self):
	# 	csrf = "xyz"

	# 	if not u'csrf_token' in post.keys():
	# 		post.update({
	# 			'csrf_token':csrf
	# 			})
	# 	request = testing.DummyRequest(post)
	# 	request.session = Mock()
	# 	csrf_token = Mock()
	# 	csrf_token.return_value = csrf 
	# 	request.session.get_csrf_token = csrf_token
	# 	return request 

		


	def add_rating(self, user_id, movie_id, value):	
		return self.app.post('/rating', data=dict(
			user_id = user_id,
    		value = value,
    		movie_id = movie_id
    		), follow_redirects=True)


		# value = 3
		# user_id=1
		# movie_id=1

		# with self.app as c:
	 #    		with c.session_transaction() as session:
	 #    			session['user_id'] = 1
	    			
	    		
		# 		response = self.add_rating(1, 1, 3)
		# 		print response.data
		# 		assert "Your rating has been updated" in response.data

	# def test_add_rating(self):
	# 	with judgement.app.request_context('/rating'):
	# 		assert request.method=='POST'

	# def wsgi_app(self, environ):
 #    with self.request_context(environ):
 #        try:
 #            response = self.full_dispatch_request()
 #        except Exception, e:
 #            response = self.make_response(self.handle_exception(e))
 #        return response(environ, start_response)


    
 #    def test_update_existing_rating(self):


 #    rating = db_session.query(Rating).filter(Rating.user_id==user_id).filter(Rating.movie_id==movie_id).first()

 #    if not rating:
 #        flash("Your rating has been added")
 #        rating = Rating()
 #        rating.user_id = user_id
 #        rating.movie_id = movie_id
 #        rating.rating = int(value)
 #        db_session.add(rating)
 #        db_session.commit()

   
 #    else:
 #        flash("Your rating has been updated")    
 #        rating.rating = int(value)
       
 #    db_session.commit()
 #    return redirect (url_for('display_movie', id=movie_id))



    
 #    rating = db_session.query(Rating).filter(Rating.user_id==user_id).filter(Rating.movie_id==movie_id).first()

 #    if not rating:
 #        flash("Your rating has been added")
 #        rating = Rating()
 #        rating.user_id = user_id
 #        rating.movie_id = movie_id
 #        rating.rating = int(value)
 #        db_session.add(rating)
 #        db_session.commit()


	# def add_rating(self):
	# 	return self.app.get('/rating?=<int:id>', follow_redirects=True)





# class TestRequests(unittest.TestCase):
# 	def setUp(self):
# 		self.app = judgement.app 

# 	def test_requests(self):
		
# 		with self.app.test_request_context('/movie/?id=1'):
# 			assert judgement.request.path == '/movie'
# 			assert judgement.request.args['id'] == '1'

# 	with app.test_request_context()

# class TestRequests(unittest.TestCase):

	


	# def test_mock_objects():
	# 	myobject = mock.Mock()
	# 	mock_return_value = {'fake':'value'}
	# 	myobject.function = mock.Mock(return_value=mock_return_value)
	# 	returned = myobject.function()
	# 	assert returned == mock_return_value
	# 	print "This is true or false", returned==mock_return_value
	# def test_set_date_range(self):
 #    arg_dict = {
 #            'min_date': "2011-7-1",
 #            'max_date': "2011-7-4",
 #    }
 #    with self.app.test_request_context('/date_range/',
 #                method="POST", data=arg_dict):

 #        # call the before funcs
 #        rv = self.app.preprocess_request()
 #        if rv != None:
 #            response = self.app.make_response(rv)
 #        else:
 #            # do the main dispatch
 #            rv = self.app.dispatch_request()
 #            response = self.app.make_response(rv)

 #            # now do the after funcs
 #            response = self.app.process_response(response)

 #    assert response.mimetype == 'application/json'
 #    assert "OK" in response.data








		


if __name__=="__main__":
	unittest.main()