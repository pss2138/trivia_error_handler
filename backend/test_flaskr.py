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
        # please replace the database YOURPASSWORD place.
        self.database_path = "postgres://postgres:YOURPASSWORD@localhost:5432/trivia"
        setup_db(self.app, self.database_path)

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

    def test_paginate_questions(self):
        """ Test questions pagination """
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_num'])
        self.assertTrue(len(data['questions']))

    def test_wrong_request_on_valid_page(self):
        """ Test 404 error works """
        response = self.client().get('/quetions?page=500')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_get_categories(self):
        """ Test categories page """
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_request_non_existing_category(self):
        """ Test categories page 404 error works"""
        response = self.client().get('categories/500')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_get_questions(self):
        """ Test questions page """
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_delete_question(self):
        """ Test deleting question works """
        question = Question(question='test question', answer='test answer', category='1', difficulty=1)
        question.insert()
        question_id = question.id

        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)

        question = Question.query.filter(Question.id == question.id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], str(question_id))

    def test_wrong_request_on_delete_question(self):
        """ Test unexisting data request on delete question """
        response = self.client().delete('/questions/500')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_create_question(self):
        """ Test create question """
        test_question = {'question': 'test question', 'answer': 'test answer', 'category': '1', 'difficulty': 1}

        questions_before = len(Question.query.all())
        response = self.client().post('/questions', json=test_question)
        data = json.loads(response.data)
        questions_after = len(Question.query.all())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(questions_after - questions_before == 1)

    def test_unfilled_request_create_question(self):
        """ Test unfilled data request on create question """
        test_question = {'question': 'test question', 'answer': 'test answer', 'category': '1'}

        response = self.client().post('/questions', json=test_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")
        
    def test_search_questions(self):
        """ Test search questions """
        response = self.client().post('/questions/search', json={'searchTerm': 'winter'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])

    def test_request_null_data_search_questions(self):
        """ Test null data request on search questions """
        response = self.client().post('/questions/search', json={'searchTerm': ''})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_get_questions_by_category(self):
        """ Test get_questions_by_category """
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['question_num'])
        self.assertTrue(data['current_category_name'])
        self.assertTrue(data['current_category'])

    def test_wrong_request_on_quesitons_by_category(self):
        """ Test wrong request on questions by category """
        response = self.client().get('/categories/a/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_get_quiz(self):
        test_quiz = {'previous_questions': [15, 16], 'quiz_category': {'type': 'Science', 'id': "1"}}

        response = self.client().post('/quizzes', json=test_quiz)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 1)
        self.assertTrue(data['question']['id'], 15)
        self.assertTrue(data['question']['id'], 16)

    def test_request_no_data_get_quiz(self):
        """ Test request without on get quiz """
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()