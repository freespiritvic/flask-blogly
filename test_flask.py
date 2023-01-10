from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Tests for users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        users = User(first_name='Slim', last_name='Pickens')
        db.session.add(users)
        db.session.commit()

        self.user_id = users.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_user(self):
        """testing for user list"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Slim Pickens', html)

    def test_show_user(self):
        """Test for showing user"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Slim Pickens', html)

    def test_add_user(self):
        """Test for adding user"""
        with app.test_client() as client:
            resp = client.post("/users/new", data={"first-name":"New", "last-name":"User", "image-url":""},follow_redirects=True)
            user = User.query.filter_by(last_name="User").first()
             
            self.assertEqual(user.first_name, "New")

    def test_delete_user(self):
        """Test for deleting user"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete")
            user = User.query.get(self.user_id)

            self.assertTrue(user)

class PostTestCase(TestCase):
    """Tests for posts."""

    def setUp(self):
        """Add sample post."""

        Post.query.delete()

        posts = Post(first_name='Slim', last_name='Pickens')
        db.session.add(posts)
        db.session.commit()

        self.user_id = posts.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_user(self):
        """testing for user list"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Slim Pickens', html)

    def test_show_user(self):
        """Test for showing user"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Slim Pickens', html)

    def test_add_user(self):
        """Test for adding user"""
        with app.test_client() as client:
            resp = client.post("/users/new", data={"first-name":"New", "last-name":"User", "image-url":""},follow_redirects=True)
            user = User.query.filter_by(last_name="User").first()
             
            self.assertEqual(user.first_name, "New")

    def test_delete_user(self):
        """Test for deleting user"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete")
            user = User.query.get(self.user_id)

            self.assertTrue(user)
            