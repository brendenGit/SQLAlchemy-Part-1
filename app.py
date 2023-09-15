"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_db"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'sage123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()


@app.route("/")
def view_users():
    """list all users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users")
def list_users():
    """list all users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/new", methods=['GET', 'POST'])
def add_user():
    """add/create user"""

    if request.method == 'GET':
        return render_template("add_user.html")

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        profile_picture = request.form['prof_pic']

        user = User(first_name=first_name, last_name=last_name,
                    profile_picture=profile_picture)
        db.session.add(user)
        db.session.commit()

        return redirect(f"/users/{user.id}")


@app.route("/users/<int:user_id>", methods=['GET', 'POST'])
def view_user(user_id):
    """view a specific users details"""

    if request.method == 'POST':
        action = request.form['action']

        if action == 'cancel':
            # Handle the cancel action
            return redirect(f"/user_info/{user_id}")

        elif action == 'save':
            return "test"

    user = User.query.get_or_404(user_id)
    posts = user.posts

    return render_template("user_detail.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit", methods=['GET', 'POST'])
def edit_user(user_id):
    """edit a specific user"""

    if request.method == 'GET':
        user = User.query.get_or_404(user_id)
        return render_template("edit_user.html", user=user)

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        profile_picture = request.form['prof_pic']

        user = User.query.get(user_id)

        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.profile_picture = profile_picture
            db.session.commit()

            return redirect(f"/users/{user.id}")

        else:
            return "User not found", 404


@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    """delete a specific user"""

    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()

        return redirect('/users')
    else:
        return "User not found", 404


@app.route("/users/<int:user_id>/posts/new", methods=['GET', 'POST'])
def add_post(user_id):
    """add a post"""

    if request.method == 'GET':
        user = User.query.get_or_404(user_id)
        tags = Tag.query.all()
        return render_template("add_post.html", user=user, tags=tags)

    elif request.method == 'POST':
        title = request.form['post_title']
        content = request.form['post_content']
        tags = request.form.getlist('tags')

        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()

        for tag in tags:
            post_tag = PostTag(tag_name=tag, post_id=post.id)
            db.session.add(post_tag)

        db.session.commit()

        return redirect(f"/posts/{post.id}")


@app.route("/posts/<int:post_id>")
def view_post(post_id):
    """view a specific post details"""

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    print(tags)

    return render_template("post_detail.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=['GET', 'POST'])
def edit_post(post_id):
    """edit a specific post"""

    if request.method == 'GET':
        post = Post.query.get_or_404(post_id)
        associated_tags = post.tags
        tags = Tag.query.all()

        return render_template("edit_post.html", post=post, tags=tags, associated_tags=associated_tags)

    elif request.method == 'POST':
        title = request.form['post_title']
        content = request.form['post_content']
        tags = request.form.getlist('tags')
        print(f'tags --------- {tags}')

        post = Post.query.get(post_id)

        if post:
            post.title = title
            post.content = content
            db.session.commit()

            associated_tags = post.tags
            for tag in associated_tags:
                post_tag = PostTag.query.filter_by(
                    tag_name=tag.tag_name, post_id=post_id).first()
                if post_tag:
                    db.session.delete(post_tag)

            db.session.commit()
            for tag in tags:
                post_tag = PostTag(tag_name=tag, post_id=post.id)
                db.session.add(post_tag)

            db.session.commit()

            return redirect(f"/posts/{post.id}")

        else:
            return "User not found", 404


@app.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    """delete a specific post"""

    post = Post.query.get(post_id)
    user_id = post.user.id

    if post:
        db.session.delete(post)
        db.session.commit()

        return redirect(f'/users/{user_id}')
    else:
        return "Post not found", 404


@app.route("/tags")
def list_tags():
    """list all tags"""

    tags = Tag.query.all()
    return render_template("tag_list.html", tags=tags)


@app.route("/tags/<tag_name>")
def view_tag(tag_name):
    """view a specific tag"""

    tag = Tag.query.get_or_404(tag_name)
    associated_posts = Post.query.join(PostTag).join(
        Tag).filter(Tag.tag_name == tag.tag_name).all()

    return render_template("view_tag.html", tag=tag, associated_posts=associated_posts)


@app.route("/tags/new", methods=['GET', 'POST'])
def add_tag():
    """add a tag"""

    if request.method == 'GET':
        return render_template("add_tag.html")

    elif request.method == 'POST':
        tag_name = request.form['tag_name']

        tag = Tag(tag_name=tag_name)
        db.session.add(tag)
        db.session.commit()

        return redirect(f"/tags")


@app.route("/tags/<tag_name>/edit", methods=['GET', 'POST'])
def edit_tag(tag_name):
    """edit a specific post"""

    if request.method == 'GET':
        tag = Tag.query.get_or_404(tag_name)
        return render_template("edit_tag.html", tag=tag)

    elif request.method == 'POST':
        new_tag_name = request.form['new_tag_name']

        new_tag = Tag(tag_name=new_tag_name)
        db.session.add(new_tag)
        db.session.commit()

        PostTag.query.filter_by(tag_name=tag_name).update({"tag_name": new_tag_name})
        db.session.commit()

        old_tag = Tag.query.filter_by(tag_name=tag_name).first()
        if old_tag:
            db.session.delete(old_tag)
            db.session.commit()
            return redirect(f"/tags/{new_tag_name}")
        else:
            return "Tag not found", 404


@app.route("/tags/<tag_name>/delete", methods=['POST'])
def delete_tag(tag_name):
    """delete a tag"""

    tag = Tag.query.get(tag_name)

    if tag:
        db.session.delete(tag)
        db.session.commit()

        return redirect(f'/tags')
    else:
        return "Post not found", 404
