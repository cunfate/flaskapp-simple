import unitest
from flask import current_app
from app import create_app, db
from app.main import User


class BasicTestCase(unitest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)


class UserModelTestCase(unitest.TestCase):
    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_password_verify(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('doggy'))

    def test_password_hash_is_random(self):
        u = User(password='cat')
        n = User(password='cat')
        self.assertFalse(u.password_hash == n.password_hash)
