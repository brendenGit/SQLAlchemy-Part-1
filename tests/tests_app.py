from unittest import TestCase
from app import app
from flask import session, render_template
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="Brenden", last_name="Arias", profile_picture='https://media.gq-magazine.co.uk/photos/5d13a04bb744d364a425653b/1:1/w_1280,h_1280,c_limit/The-Big-Lebowski-hp-GQ-25Feb16_rex_b.jpg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Brenden', html)

    def test_create_user(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

        with app.test_client() as client:
            data = {
                "first_name": "Meghan",
                "last_name": "Hart",
                "prof_pic": "test"
            }
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="user-h1">Meghan Hart</h1>', html)

    def test_view_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Brenden Arias', html)

    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a user</h1>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)