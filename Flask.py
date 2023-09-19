from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')#, 'postgresql://bahadr:password@localhost/flask')
db = SQLAlchemy(app)
api = Api(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")

class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(400))
    firstname = db.Column(db.String(400))
    middlename = db.Column(db.String(400))
    lastname = db.Column(db.String(400))
    birthdate = db.Column(db.String(400))
    email = db.Column(db.String(400))
    password = db.Column(db.String(500))

    def __init__(self, username, firstname, middlename, lastname, birthdate, email, password):
        self.username = username
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.birthdate = birthdate
        self.email = email
        self.password = password 

    def __repr__(self):
        return f"<User {self.username}>"

class OnlineUsers(db.Model):
    __tablename__ = 'OnlineUsers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    ipaddress = db.Column(db.String(40))
    logindatetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, ipaddress):
        self.username = username
        self.ipaddress = ipaddress

    def __repr__(self):
        return f"<OnlineUser {self.username}>"

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("home.html")

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Users.query.filter_by(username=username).first()  
        if user and sha256_crypt.verify(password, user.password): 
            login_user(user)
            online_user = OnlineUsers(username=username, ipaddress=request.remote_addr)
            db.session.add(online_user)
            db.session.commit()
            
            return redirect(url_for('welcome', username=username))  
        else:
            error = "Invalid username or password."
            return render_template('home.html', error=error)
    
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required  
def logout():
    online_user = OnlineUsers.query.filter_by(username=current_user.username).first()
    if online_user:
        db.session.delete(online_user)
        db.session.commit()

    logout_user()
    return redirect(url_for('home')) 





@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)  

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        email = request.form['email']
        password = sha256_crypt.encrypt(request.form['password'])
        
        new_user = Users(username=username, firstname=firstname, middlename=middlename,
                         lastname=lastname, birthdate=birthdate, email=email, password=password)
        
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  
    else:
        return render_template("Sign.html")
    
    
    
@app.route('/user_action', methods=['GET', 'POST'])
def user_action():
    if request.method == 'POST':
        user_id = request.form.get('id')
        if user_id:
            user = Users.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
    users = Users.query.all()
    return render_template('user_action.html', users=users)

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = Users.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('user_action'))


@app.route('/update_user')
def update_user():
    users = Users.query.all()
    return render_template('update_user.html', users=users)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user = Users.query.get(id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.firstname = request.form['firstname']
        user.middlename = request.form['middlename']
        user.lastname = request.form['lastname']
        user.birthdate = request.form['birthdate']
        user.email = request.form['email']
        
        
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        if new_password and confirm_password and new_password == confirm_password:
            user.password = sha256_crypt.encrypt(new_password)
        
        db.session.commit()
        
        return redirect(url_for('login'))
        
    return render_template('update.html', user=user)


@app.route('/online_users')
def online_users():
    online_users = OnlineUsers.query.all()
    return render_template('online_users.html', online_users=online_users)   

def is_active(self):
        return True
    
class UserListResource(Resource):
    def get(self):
        pass

    def post(self):
        pass

class UserResource(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

class OnlineUsersResource(Resource):
    def get(self):
        
        pass

api.add_resource(UserListResource, '/user/list')
api.add_resource(UserResource, '/user/<int:id>')
api.add_resource(OnlineUsersResource, '/onlineusers')

if __name__ == "__main__":  
 app.run(debug=True,host="0.0.0.0")
 print("Flask uygulamanız başarıyla başladı.")