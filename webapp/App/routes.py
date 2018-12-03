import secrets
import os
from flask import request,render_template,url_for,redirect,flash
from App.login import registration,loginform,UpdateForm
from App.models import User,Movie
from App import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required
from PIL import Image
data =[
    {
        'movie':'Inception',
        'released':"yes",
        'on':"10 AUG 2015",
        'rating':'9',
    },  
    {
        'movie':'Thugs of hindostan',
        'released':"yes",
        'on':"10 NOV 2018",
        'rating':'-5',
    },
    {
        'movie':'Interstellar',
        'released':"yes",
        'on':"10 AUG 2016",
        'rating':'10',
    }
]



@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html',movies=data)

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



