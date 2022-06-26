import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.sample_question = {
            'question': 'What is the capital city of Kenya?',
            'answer': 'Nairobi',
            'category': 3,
            'difficulty': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #tests get all categories 
    def test_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        
    #test for get questions    
    def test_get_questions(self):
        response = self.client().get('/questions?page=1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['questions'], list)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertIsInstance(data['total_questions'], int)
        self.assertIsInstance(data['categories'], dict)
    #Tests delete_question with an id of 2   
    def test_delete_question(self):
        response = self.client().delete('/questions/2')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'],2)
        if response.status_code == 404:
            self.assertEqual(data['success'], False)
        else:
            self.assertEqual(data['deleted'], 2)
     
    #test delete error when a wrong id is issued
    def test_delete_question_failerror(self):
        response = self.client().delete('/questions/8374')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    
    #Test for create_question  
    def test_create_question(self):
        response = self.client().post('/questions', questn=json.dumps(self.sample_question), content_type = 'application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_question_fail(self):
        response = self.client().post('/questions/9847', questn=json.dumps(self.sample_question))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    #Test search    
    def test_search(self):
        response = self.client().post('/questions', json={'searchTerm': 'Hackers'})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['total_questions'], int)
    #Test search with no results
    def test_search_error(self):
        response = self.client().post('/questions', json={'searchTerm':'asdf'})

        data = json.loads(response.data)

        self.assertEqual(data['total_questions'],0)
        self.assertEqual(data['success'], True)
    
    #Test for question by categories    
    def test_get_questions_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['current_category'], 'Capital Cities')
        self.assertEqual(data['success'], True)
    
    #test question by categories using a cateegory that doesn't exist.
    def test_get_questions_by_category_404(self):
        response = self.client().get('/categories/8768/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        
    
    def test_play_quiz_game(self):
        quiz_round = {'previous_questions': [1, 2, 3, 4], 'quiz_category': {'type': 'History', 'id': 10}}
        response = self.client().post('/quizzes', json=quiz_round)
        data = json.loads(response.data)

        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_422_quiz(self):
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()