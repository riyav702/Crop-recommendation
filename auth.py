from flask import Blueprint, render_template, request, redirect, session
from pymongo import MongoClient

auth_bp = Blueprint('auth', __name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["crop_recommendation"]
users_collection = db["users"]

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username, 'password': password})

        if user:
            session['username'] = username
            return redirect('/home')
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return render_template('signup.html', error="Username already exists")

        users_collection.insert_one({'username': username, 'password': password})
        return redirect('/login')
    
    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')
