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
        User.query.delete()

        post = Post(title="Sample Title", content="Sample Content", created_at='4/6/22')
        user = User(first_name='Test', last_name='User', image_url='')
        db.session.add(post)
        db.session.add(user)
        db.session.flush()
        db.session.commit()

        self.post_id = post.id
        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_post(self):
        """testing for showing a post"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Sample Title', html)

    def test_edit_post(self):
        """Test for editing a post"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit", data={'title': 'Sample Title', 'content': 'Test Content'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Sample Title', html)

    def test_add_post(self):
        """Test for adding a post"""
        with app.test_client() as client:
            resp = client.post(f'users/{self.user_id}/posts/new',
                               data={'title': 'Test New Post', 'content': 'Test Content'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            post = Post.query.filter_by(content='Test Content').first()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(post.title, 'Test New Post')

    def test_delete_post(self):
        """Test for deleting a post"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/delete")
            post = Post.query.get(self.post_id)

            self.assertTrue(post)
            

