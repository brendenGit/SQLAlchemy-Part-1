"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
def create_user():
    """add/create user"""

    if request.method == 'GET':
            return render_template("create_user.html")
    
    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        profile_picture = request.form['prof_pic']

        user = User(first_name=first_name, last_name=last_name, profile_picture=profile_picture)
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
    return render_template("user_detail.html", user=user)


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


