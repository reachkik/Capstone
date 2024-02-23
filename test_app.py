import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from models import db, setup_db

class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.casting_assistant_auth={'Authorization':'Bearer ' + os.getenv("CASTING_ASSISTANT_TOKEN")}
        self.casting_director_auth={'Authorization':'Bearer ' + os.getenv("CASTING_DIRECTOR_TOKEN")}
        self.executive_producer_auth={'Authorization':'Bearer ' + os.getenv("EXECUTIVE_PRODUCER_TOKEN")}
        self.executive_producer_auth_expired={'Authorization':'Bearer ' + os.getenv("EXECUTIVE_PRODUCER_TOKEN_EXPIRED")}
        '''
        load_dotenv()
        self.db_user=os.getenv("DB_USERNAME")
        self.db_password=os.getenv("DB_PASSWORD")
        self.db_hostname=os.getenv("DB_HOSTNAME")
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.db_user,self.db_password,self.db_hostname, self.database_name)
        '''
        self.database_path = os.environ['TEST_DATABASE_URL']
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Positive and negative test for each endpoint.
    """

    # End point get /actors: Postive and Negative tests
    # This is also the positive test case for RBAC role Casting Assistant
    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.casting_assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])
    
    def test_get_actors_404_method_not_allowed(self):
        res = self.client().get('/actors/1', headers=self.casting_assistant_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'method not allowed')

    # End point get /movies: Postive and Negative tests
    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.casting_assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])
    
    def test_get_movies_404_method_not_allowed(self):
        res = self.client().get('/movies/5', headers=self.casting_assistant_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'method not allowed')

    # End point put /actors: Postive and Negative tests
    # This is also the positive test case for RBAC role Casting Director
    def test_add_actor(self):
        self.new_actor = {"name":"Dwayne Johnson", "gender":"M", "age":"51"}
        res = self.client().post('/actors', json=self.new_actor, headers=self.casting_director_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id_added'])
    
    def test_add_actor_422_unprocessable_entity(self):
        self.new_actor = {"name":"Dwayne Johnson", "age":"51"}
        res = self.client().post('/actors', json=self.new_actor, headers=self.casting_director_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')

    # End point put /movies: Postive and Negative tests
    def test_add_movie(self):
        self.new_movie = {"title":"Gladiator", "release_date":"2000-09-01"}
        res = self.client().post('/movies', json=self.new_movie, headers=self.executive_producer_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id_added'])
    
    def test_add_movie_422_unprocessable_entity(self):
        self.new_movie = {"title":"Gladiator"}
        res = self.client().post('/movies', json=self.new_movie, headers=self.executive_producer_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')

    # End point patch /actors: Postive and Negative tests
    def test_patch_actor(self):
        self.patch_actor = {"age":"59"}
        res = self.client().patch('/actors/1', json=self.patch_actor, headers=self.casting_director_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id_updated'])
    
    def test_patch_actor_404_resource_not_found(self):
        self.patch_actor = {"age":"59"}
        res = self.client().patch('/actors/100', json=self.patch_actor, headers=self.casting_director_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # End point put /movies: Postive and Negative tests
    def test_patch_movie(self):
        self.patch_movie = {"title":"Iris 2001"}
        res = self.client().patch('/movies/1', json=self.patch_movie, headers=self.casting_director_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id_updated'])
    
    def test_patch_movie_404_resource_not_found(self):
        self.patch_movie = {"title":"Iris 2001"}
        res = self.client().patch('/movies/100', json=self.patch_movie, headers=self.casting_director_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # End point delete /actors: Postive and Negative tests
    def test_delete_actor(self):
        res = self.client().delete('/actors/14', headers=self.casting_director_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
    
    def test_delete_actor_404_resource_not_found(self):
        res = self.client().delete('/actors/100', headers=self.casting_director_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # End point delete /movies: Postive and Negative tests
    # This is also the positive test case for RBAC role Executive Producer
    def test_delete_movie(self):
        res = self.client().delete('/movies/14', headers=self.executive_producer_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
    
    def test_delete_movie_404_resource_not_found(self):
        res = self.client().delete('/movies/100', headers=self.executive_producer_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # This is a negative test case for RBAC role Casting Director
    def test_delete_movie_RBAC_negative(self):
        res = self.client().delete('/movies/15', headers=self.casting_director_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], {'code': 'unauthorized', 'description': 'Permission not found.'})

    # This is a negative test case for RBAC role Casting Assistant
    def test_add_actor_RBAC_negative(self):
        self.new_actor = {"name":"Dwayne Johnson", "gender":"M", "age":"51"}
        res = self.client().post('/actors', json=self.new_actor, headers=self.casting_assistant_auth)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], {'code': 'unauthorized', 'description': 'Permission not found.'})

    # This is a negative test case for RBAC role Executive Producer
    def test_patch_movie_RBAC_negative(self):
        self.patch_movie = {"title":"Iris 2001"}
        res = self.client().patch('/movies/100', json=self.patch_movie, headers=self.executive_producer_auth_expired)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], {'code': 'token_expired', 'description': 'Token expired.'})
 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
