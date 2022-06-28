import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'trivia_test')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
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
        self.assertTrue(data.get('categories'))
        self.assertTrue(data.get('success'))
        
        
    #test for get questions    
    def test_get_questions(self):
        response = self.client().get('/questions?page=1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data.get('categories'))
        self.assertTrue(data.get('questions'))
        self.assertTrue(data.get('success'))
        
    def test_404_for_unavailable_questions_pages(self):
        res = self.client().get("/questions?page=6876")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
            
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
            
            
    #Testing successful deletion        
    def test_delete_question(self):
        question = {
        'question': 'Capital of USA',
        'answer': 'Washington DC',
        'difficulty': 1,
        'category': 1,
    }
        operation_res = self.client().post('/questions', json=question)
        result_data = json.loads(operation_res.data)

        res = self.client().delete(
            '/questions/{}'.format(result_data.get('question_id'))
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('deleted_id'), str(result_data.get('question_id'))
        )
        self.assertTrue(data.get('success'))
     
    #test delete error when a wrong id is issued
    def test_delete_question_failerror(self):
        response = self.client().delete('/questions/8374')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        
            
    #Test for create_question  
    def test_create_question(self):
        response = self.client().post('/questions', questn=json.dumps(self.sample_question), content_type = 'application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        
        
    #Tests creation with missing attributes    
    def test_create_question_fail(self):
        question = {
            'answer': 'Kigali',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=question)
        self.assertEqual(res.status_code, 400)
        
            
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
        
            
    #Test for question by categories    
    def test_get_questions_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('questions'))
        
        
    #test question by categories using a cateegory that doesn't exist.
    def test_get_questions_by_category_404(self):
        response = self.client().get('/categories/8768/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        
         
    def test_play_quiz_game(self):
        quiz_round = {'previous_questions': [], 'quiz_category': {'type': 'General History', 'id': 3}}
        response = self.client().post('/quizzes', json=quiz_round)
        data = json.loads(response.data)

        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('question'))
        
        
    def test__play_quiz_game_fail(self):
        data = {
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=data)
        self.assertEqual(res.status_code, 400)
        
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()