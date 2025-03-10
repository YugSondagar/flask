from grocerylist import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):  #it is the one thing through which extension will work bcoz extention requires one thing through which it will pick user from id
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
    
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Items('{self.name},{self.quantity},{self.category}')"