from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin    #UserMixin is a helper class provided by Flask-Login that makes it easier to implement user authentication in a Flask app.

@login_manager.user_loader
def load_user(user_id):  #it is the one thing through which extension will work bcoz extention requires one thing through which it will pick user from id
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    username = db.Column(db.String(20),unique = True,nullable=False)
    email = db.Column(db.String(120),unique = True,nullable=False)    
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg') 
    password = db.Column(db.String(60),nullable=False) 
    posts = db.relationship('Post',backref='author',lazy=True)   #here we are refering to class Post
    
    # remember the post is not a column in table it is an additional query which graps any post from user

    def get_reset_token(self, expires_sec=1800):
        s = serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
 
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted= db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)   #in foreign key we are referencing user table name and column name

    def __repr__(self):
        return f"Post('{self.id}',{self.date_posted}')"