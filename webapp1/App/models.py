from App import db,login_manager
from datetime import datetime
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


likes = db.Table('likes',
db.Column('id',db.Integer,db.ForeignKey('user.id')),
db.Column('movie_id',db.Integer,db.ForeignKey('movie.id')),
db.Column('rating_given',db.Integer,default=0)
)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.png')
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"Name:{self.username},Email:{self.email},id:{self.id}"
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    rating = db.Column(db.Float,nullable=False,default=0)
    image = db.Column(db.String(90),nullable=False,default='default_img.png')
    like = db.relationship('User',secondary=likes,backref=db.backref('like',lazy='dynamic'))
    Genre=db.Column(db.String(100))
    Action=db.Column(db.Integer,nullable=False)
    Adventure=db.Column(db.Integer,nullable=False)
    Animation=db.Column(db.Integer,nullable=False)
    Comedy=db.Column(db.Integer,nullable=False)
    Crime=db.Column(db.Integer,nullable=False)
    Documentary=db.Column(db.Integer,nullable=False)
    Drama=db.Column(db.Integer,nullable=False)
    Family=db.Column(db.Integer,nullable=False)
    Fantasy=db.Column(db.Integer,nullable=False)
    Foreign=db.Column(db.Integer,nullable=False)
    History=db.Column(db.Integer,nullable=False)
    Horror=db.Column(db.Integer,nullable=False)
    Music=db.Column(db.Integer,nullable=False)
    Mystery=db.Column(db.Integer,nullable=False)
    Romance=db.Column(db.Integer,nullable=False)
    Science_Fiction=db.Column(db.Integer,nullable=False)
    Tv_Movie=db.Column(db.Integer,nullable=False)
    Thriller=db.Column(db.Integer,nullable=False)
    War=db.Column(db.Integer,nullable=False)
    Western=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Movie:{self.name},rating:{self.rating}"

