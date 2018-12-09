import secrets
import os
from flask import request,render_template,url_for,redirect,flash
from App.login import registration,loginform,UpdateForm,create_area
from App.models import User,Movie
from App import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required
from PIL import Image
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sqlalchemy.sql.expression import func,select
import random
movies = Movie.query.filter(Movie.rating>8.0).all()
top_movies = Movie.query.filter(Movie.rating>9.0).all()


def random_top():
    li = [x.id for x in movies]
    random.shuffle(li)
    movie=[]
    for x in li:
        movie.append(Movie.query.filter_by(id=x).first())
    return movie[:12]

def top_searched():
    li = [x.id for x in top_movies]
    random.shuffle(li)
    movie=[]
    for x in li:
        movie.append(Movie.query.filter_by(id=x).first())
    return movie[:12]



df = pd.read_csv('new_movie_data.csv')
X=df.iloc[:,5:25]
nbrs=NearestNeighbors(n_neighbors=9).fit(X)

def recommend(genre):
    li = list(nbrs.kneighbors([genre]))
    li=li[1].flatten()
    movie=[]
    for x in li:
        x=int(x)
        movie.append(Movie.query.filter_by(id=x).first())
    return movie

@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
def home():
    form = create_area()
    rated=[]
    genre=[]
    recommended=[]
    
    if form.validate_on_submit and current_user.is_authenticated:
        val = form.text_area.data
        movie = form.movie.data
        id = current_user.get_id()
        if val and int(val):
            user = User.query.filter_by(id=id).first()
            movie = Movie.query.filter_by(name=movie).first()
            user.like.append(movie)
            genre = [movie.Action,movie.Adventure,movie.Animation,movie.Comedy,movie.Crime,movie.Documentary,movie.Drama,movie.Family,movie.Fantasy,movie.Foreign,movie.History,movie.Horror,movie.Music,movie.Mystery,movie.Romance,movie.Science_Fiction,movie.Tv_Movie,movie.Thriller,movie.War,movie.Western]
            recommended = recommend(genre)
            db.session.commit()
            flash(f'You have rated {movie.name}  {val}  Stars....','success')
        rated = [x.name for x in current_user.like]
    movie = random_top()
    return render_template('index.html',form=form,rated=rated,movies=movie,recommended=recommended)


@app.route("/popUp")
def popUp():
    return render_template('popUp.html',title='about')

@app.route("/about")
def about():
    return render_template('about.html',title='about')

@app.route("/register",methods=['GET','POST'])
def register():
    form = registration()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_pwd)
        db.session.add(user)
        db.session.commit() 
        flash(f'Your Account is successfully created! You are ready to Log In  ','success')
        return redirect(url_for('login'))
    return render_template("register.html",title="register",form = form)
@app.route("/login",methods=['GET','POST'])
def login():
    form= loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next') #this next variable is seen when we manually type the route...
            if next_page:
                next_page = next_page[1:]
            flash(f'You have successfully logged in!','success')
            return redirect(url_for(next_page)) if next_page else redirect(url_for('home'))
        else:
            flash(f'Error! There must be something wrong','danger')

    return render_template("login.html",title="register",form = form)


#logout route that wil redirect to home 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



def save_picture(form_picture):
    picture_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = picture_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/assets',picture_fn)
    form_picture.save(picture_path)
    return picture_fn



#this is account route which is only be allowed to access if user is user is authenticated
@app.route('/account',methods=['GET','POST'])
@login_required #this is used to keep track if user is authenticated or not
def account():
    form=UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_name = save_picture(form.picture.data)
            current_user.image_file = picture_name
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename="assets/"+current_user.image_file)
    return render_template('account.html',title='Account',image=image_file,form=form)

@app.route('/most_searched',methods=['GET','POST'])
def most():
    form=create_area()
    movie=top_searched()
    recommended=[]
    if form.validate_on_submit and current_user.is_authenticated:
        val = form.text_area.data
        movie = form.movie.data
        id = current_user.get_id()
        if val and int(val):
            user = User.query.filter_by(id=id).first()
            movie = Movie.query.filter_by(name=movie).first()
            user.like.append(movie)
            genre = [movie.Action,movie.Adventure,movie.Animation,movie.Comedy,movie.Crime,movie.Documentary,movie.Drama,movie.Family,movie.Fantasy,movie.Foreign,movie.History,movie.Horror,movie.Music,movie.Mystery,movie.Romance,movie.Science_Fiction,movie.Tv_Movie,movie.Thriller,movie.War,movie.Western]
            recommended = recommend(genre)
            db.session.commit()
            flash(f'You have rated {movie.name}  {val}  Stars....','success')
        rated = [x.name for x in current_user.like]
    movie = random_top()
    return render_template('most.html',movies=movie,form=form)

@app.route('/latest',methods=['GET','POST'])
def latest():
    form=create_area()
    movie=top_searched()
    recommended=[]
    if form.validate_on_submit and current_user.is_authenticated:
        val = form.text_area.data
        movie = form.movie.data
        id = current_user.get_id()
        if val and int(val):
            user = User.query.filter_by(id=id).first()
            movie = Movie.query.filter_by(name=movie).first()
            user.like.append(movie)
            genre = [movie.Action,movie.Adventure,movie.Animation,movie.Comedy,movie.Crime,movie.Documentary,movie.Drama,movie.Family,movie.Fantasy,movie.Foreign,movie.History,movie.Horror,movie.Music,movie.Mystery,movie.Romance,movie.Science_Fiction,movie.Tv_Movie,movie.Thriller,movie.War,movie.Western]
            recommended = recommend(genre)
            db.session.commit()
            flash(f'You have rated {movie.name}  {val}  Stars....','success')
        rated = [x.name for x in current_user.like]
    movie = random_top()
    return render_template('most.html',movies=movie,form=form)

@app.route('/top',methods=['GET','POST'])
def top():
    form=create_area()
    movie=top_searched()
    recommended=[]
    if form.validate_on_submit and current_user.is_authenticated:
        val = form.text_area.data
        movie = form.movie.data
        id = current_user.get_id()
        if val and int(val):
            user = User.query.filter_by(id=id).first()
            movie = Movie.query.filter_by(name=movie).first()
            user.like.append(movie)
            genre = [movie.Action,movie.Adventure,movie.Animation,movie.Comedy,movie.Crime,movie.Documentary,movie.Drama,movie.Family,movie.Fantasy,movie.Foreign,movie.History,movie.Horror,movie.Music,movie.Mystery,movie.Romance,movie.Science_Fiction,movie.Tv_Movie,movie.Thriller,movie.War,movie.Western]
            recommended = recommend(genre)
            db.session.commit()
            flash(f'You have rated {movie.name}  {val}  Stars....','success')
        rated = [x.name for x in current_user.like]
    movie = random_top()
    return render_template('most.html',movies=movie,form=form)

@app.route('/action',methods=['GET','POST'])
def action():
    form=create_area()
    movie=top_searched()
    recommended=[]
    if form.validate_on_submit and current_user.is_authenticated:
        val = form.text_area.data
        movie = form.movie.data
        id = current_user.get_id()
        if val and int(val):
            user = User.query.filter_by(id=id).first()
            movie = Movie.query.filter_by(name=movie).first()
            user.like.append(movie)
            genre = [movie.Action,movie.Adventure,movie.Animation,movie.Comedy,movie.Crime,movie.Documentary,movie.Drama,movie.Family,movie.Fantasy,movie.Foreign,movie.History,movie.Horror,movie.Music,movie.Mystery,movie.Romance,movie.Science_Fiction,movie.Tv_Movie,movie.Thriller,movie.War,movie.Western]
            recommended = recommend(genre)
            db.session.commit()
            flash(f'You have rated {movie.name}  {val}  Stars....','success')
        rated = [x.name for x in current_user.like]
    movie = random_top()
    return render_template('most.html',movies=movie,form=form,recommended=recommended)
