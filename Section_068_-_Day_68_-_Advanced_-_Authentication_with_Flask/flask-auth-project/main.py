import os
from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page when @login_required fails
login_manager.login_message = "Please log in to access this page."  # Optional flash message

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(1000), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('You have already registered with that email. Please log in.', 'info')
            return redirect(url_for('login'))

        # Hash password
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )

        # Create new user
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user
        login_user(new_user)
        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('secrets'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('That email does not exist. Please try again or register.', 'error')
            return redirect(url_for('login'))

        if not check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.', 'error')
            return redirect(url_for('login'))

        # Password correct – log in
        login_user(user)
        flash('Logged in successfully.', 'success')
        return redirect(url_for('secrets'))

    return render_template('login.html')

@app.route('/secrets')
@login_required
def secrets():
    return render_template('secrets.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/download')
@login_required
def download():
    return send_from_directory(
        directory='static',
        path='files/cheat_sheet.txt',
        as_attachment=True,
        download_name='flask_cheat_sheet.txt'   # optional custom filename
    )

if __name__ == '__main__':
    app.run(debug=True)