from ToDo import db, login_manager 
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key=True,nullable=False)
    username = db.Column(db.String(20),unique = True,nullable=False)
    email = db.Column(db.String(120),unique = True,nullable=False)
    password = db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
    


class Task(db.Model):
    id = db.Column(db.Integer(),primary_key=True,nullable=False)
    context = db.Column(db.String(120),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    user = db.relationship('User', backref='tasks', lazy=True)


    def __repr__(self):
        return f"Task('{self.context}')"

