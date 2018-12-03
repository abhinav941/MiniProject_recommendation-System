from App import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.png')
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f'User("{self.username}","{self.email}","{self.image_file}")'

class Movie(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    date_realeased=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    description=db.Column(db.Text,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default='default.png')
    rating=db.Column(db.Integer,nullable=False,default=0)
    
    def __repr__(self):
        return f"Post('{self.name}','{self.date_realeased}'"