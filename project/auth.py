from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    """
    Render the login page.
    """
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    """
    Handle the login form submission.
    Check for empty fields, validate user credentials, and log in the user.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Check for empty fields
    if not email or not password:
        flash('Please fill out all fields.')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    """
    Render the signup page.
    """
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    """
    Handle the signup form submission.
    Check for empty fields, validate email format, check password length, and create a new user.
    """
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Check for empty fields
    if not email or not name or not password:
        flash('Please fill out all fields.')
        return redirect(url_for('auth.signup'))

    # Check for email format (simple regex for example purposes)
    import re
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash('Invalid email address.')
        return redirect(url_for('auth.signup'))

    # Check password length
    if len(password) < 6:
        flash('Password must be at least 6 characters long.')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email already exists')
        return redirect(url_for('auth.signup'))
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    db.session.add(new_user)
    db.session.commit()

    flash('Signup successful! Please log in.')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    """
    Log out the current user.
    """
    logout_user()
    return redirect(url_for('main.index'))
