
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError  
from App.models import User,Movie
from flask_login import current_user  
from flask_wtf.file import FileField,FileAllowed    

class registration(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min=2,max=20)])
    email =StringField('Email', 
                        validators=[DataRequired(),Email()])
    password = PasswordField('Password',
                            validators=[DataRequired(),Length(min=3,max=10)])
    confirm_password = PasswordField('Confirm password',
                                    validators=[DataRequired(),Length(min=3,max=10),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken! Try using other one.')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken! Try using other one.')        


class loginform(FlaskForm):
    email =StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=3,max=10)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')



class UpdateForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min=2,max=20)])
    email =StringField('Email', 
                        validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['png','jpeg','jpg'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken! Try using other one.')
    def validate_email(self,email):                  
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already taken! Try using other one.')        
