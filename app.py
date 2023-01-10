"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "simple_!$_B3TT3R"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()

@app.route('/')
@app.route('/users')
def get_users():
    """Show list of all users in db"""
    users = User.query.all()
    return render_template('users/users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def get_new_users():
    """Show a new users form & handle new form submission"""

    if request.method == 'POST':
        first = request.form["first-name"]
        last = request.form["last-name"]
        img = request.form["image-url"]

        new_user = User(first_name=first, last_name=last, image_url=img)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/users')

    return render_template('/users/new_user.html')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template('/users/details.html', user=user, posts=posts)

@app.route("/users/<int:user_id>/edit", methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit an existing user & handle edit form submission"""
    unique_user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        unique_user.first_name = request.form["first-name"]
        unique_user.last_name = request.form["last-name"]
        unique_user.image_url = request.form["image-url"]

        db.session.add(unique_user)
        db.session.commit()
        
        return redirect('/users')

    return render_template('/users/edit_page.html', unique_user=unique_user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user from db"""

    usr = User.query.get_or_404(user_id)
    db.session.delete(usr)
    db.session.commit()
    flash('User deleted.')
    return redirect('/users')

######################################## PART TWO BELOW ##################################

@app.route("/posts/<int:post_id>")
def show_posts(post_id):
    """Show a post"""
    post = Post.query.get_or_404(post_id)
    user = post.users
    tags = post.tags

    return render_template('/users/post_details.html', post=post, user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=['GET', 'POST'])
def get_new_post(user_id):
    """Create a post page & handle new post form submission"""
    
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    
    if request.method == 'POST':
        title = request.form["title"]
        content = request.form["content"]
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        new_post = Post(title=title, content=content, user_id=user.id, tags=tags)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(f'/users/{user.id}')

    return render_template('/users/new_posts.html', user=user, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=['GET', 'POST'])
def edit_post(post_id):
    """Edit an existing post & handle post form submission"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    post_tags = PostTag.query.filter_by(post_id=post.id).all()
    tag_ids = [post_tag.tag_id for post_tag in post_tags]

    if request.method == 'POST':
        post.title = request.form["title"]
        post.content = request.form["content"]

        db.session.add(post)
        db.session.commit()

        tags = request.form.getlist("tag")
        post.tags = Tag.query.filter(Tag.id.in_(tags)).all()

        db.session.add(post)
        db.session.commit()
        
        return redirect(f'/posts/{post.id}')

    return render_template('/users/edit_posts.html', post=post, tags=tags, tag_ids=tag_ids)

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post from db"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post {post.title} deleted.')
    return redirect(f'/users/{post.user_id}')

######################################## PART THREE BELOW ##################################
@app.route('/tags')
def list_tags():
    """List all tags available"""
    tags = Tag.query.all()
    return render_template('tags/tag_list.html', tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tags(tag_id):
    """Show details about a tag."""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.post_tags

    return render_template('/tags/tag_details.html', tag=tag, posts=posts)

@app.route("/tags/new", methods=['GET', 'POST'])
def get_new_tags():
    """Create a new tag & handle new tag form submission"""
    
    posts = Post.query.all()

    if request.method == 'POST':
        name = request.form["name"]
        new_tag = Tag(name=name)

        db.session.add(new_tag)
        db.session.commit()
        
        return redirect('/tags')

    return render_template('/tags/new_tag.html', posts=posts)

@app.route("/tags/<int:tag_id>/edit", methods=['GET', 'POST'])
def edit_tag(tag_id):
    """Edit an existing tag & handle tag form submission"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    if request.method == 'POST':
        tag.name = request.form["name"]

        db.session.add(tag)
        db.session.commit()
        
        return redirect('/tags')

    return render_template('/tags/edit_tag.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete tag from db"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f'Tag {tag.name} deleted.')
    return redirect('/tags')

if __name__ == "__main__":
    app.run(debug=True)