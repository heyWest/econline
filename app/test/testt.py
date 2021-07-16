import unittest
from flask import Flask, request, url_for
from flask_login import login_required

from app.extensions import db
from app.models import Voter, Election
from app.voters.routes import voters_landing


class MyTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
        self.check = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # testing routes

    def test_voters_landing(self):
        url = '/voters/confirm/<token>'
        response = self.check.get(url)
        self.assertEqual(response.status_code, 200)  # checking for expected route

    def test_admin_login(self):
        login_url = "/admin/login"
        response = self.check.get(login_url)
        self.assertEqual(response.status_code, 200)

    @login_required
    def test_admin_landing(self):
        url = "/admin/landing"
        response = self.check.get(url)
        self.assertEqual(response.status_code, 200)

    # testing rendered templates
    def test_contact_us(self):
        rv = self.check.get('/contact-us')
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Contact-us", rv.data)

    def test_thank_you(self):
        res = self.check.get('/thank-you')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Thank you!", res.data)

    
if __name__ == '__main__':
    unittest.main()
