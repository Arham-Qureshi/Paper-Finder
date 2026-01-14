import unittest
from app import create_app
from models import db, Paper
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Discover Research Papers', response.data)

    def test_paper_model(self):
        paper = Paper(id='1234.5678', title='Test Paper', summary='Abstract')
        db.session.add(paper)
        db.session.commit()
        
        p = Paper.query.get('1234.5678')
        self.assertIsNotNone(p)
        self.assertEqual(p.title, 'Test Paper')

if __name__ == '__main__':
    unittest.main()
