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
        self.database_name = "triviatest"
        self.database_path = "postgres://postgres:0000@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.newq = {'question': 'question', 'answer': 'answer',
                     'category': 2, 'difficulty': 2}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'ddef',
                                       'answer': 'ffv', 'category': 2,
                                       'difficulty': 1})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])

    def test_400_create_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'ddef',
                                       'answer': 'ffv', 'category': 'fff',
                                       'difficulty': 2})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(res.status_code, 400)

    def test_422_create_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'ddef',
                                       'answer': 'ffv', 'category': 16,
                                       'difficulty': 16})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(res.status_code, 422)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_get_questions_by_categorie(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_404_get_questions_by_categorie(self):
        res = self.client().get('/categories/33/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_404_get_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_404_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'e'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_search_question_without_result(self):
        res = self.client().post('/questions', json={'searchTerm':
                                                     'ehdghyjhthtrd'})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_delete_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        qid = data['questions'][0]['id']
        res = self.client().delete('/questions/'+str(qid))
        data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], qid)

    def test_quizzes(self):
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 2,
                                                   'type': 'Art'},
                                                   'previous_questions': []})
        data = json.loads(res.data)
        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """

# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
