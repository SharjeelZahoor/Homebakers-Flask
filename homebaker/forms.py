from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField,DecimalField,TextAreaField,EmailField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired,Length,EqualTo
from homebaker import models

class PhotoForm(FlaskForm):
    photo =FileField('Title Photo',validators=[DataRequired(),FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField("Upload")

class SeacrchForm(FlaskForm):
    q =StringField('Search',validators=[DataRequired()])
    submit = SubmitField("Go")

class RegisterForm(FlaskForm):
    loginid = StringField(label="Login ID  ",validators=[DataRequired(),Length(min=4,max=16)])
    name = StringField(label="Name  ",validators=[DataRequired(),Length(min=3,max=50)])
    contact = StringField(label="Contact  ",validators=[DataRequired(),Length(min=3,max=20)])
    email = EmailField(label="Email  ",validators=[DataRequired(),Length(max=100)])
    password = PasswordField(label="Password  ",validators=[DataRequired(),Length(min=4,max=16)])
    con_password = PasswordField("Confirm Password ",validators=[DataRequired(),Length(min=4,max=16),EqualTo('password')])
    address  = TextAreaField('Address')
    submit = SubmitField("Submit")

class ProfileForm(FlaskForm):
    name = StringField(label="Name  ",validators=[DataRequired(),Length(min=3,max=50)])
    contact = StringField(label="Contact  ",validators=[DataRequired(),Length(min=3,max=20)])
    email = EmailField(label="Email  ",validators=[DataRequired(),Length(max=100)])
    address  = TextAreaField('Address')
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    loginid = StringField(label="Login ID  ",validators=[DataRequired(),Length(min=4,max=16)])
    password = PasswordField(label="Password  ",validators=[DataRequired(),Length(min=4,max=16)])
    # con_password = PasswordField("Confirm Password : ",validators=[DataRequired(),Length(min=4,max=16),EqualTo('password')])
    submit = SubmitField("Submit")

class CakeTypeForm(FlaskForm):
    title = StringField(label="Cake Type Title  ",validators=[DataRequired(),Length(min=4,max=50)])
    submit = SubmitField("Save")

class CakeSizeForm(FlaskForm):
    title = StringField(label="Cake Size Title  ",validators=[DataRequired(),Length(min=1,max=50)])
    submit = SubmitField("Save")

class CakeFlavorForm(FlaskForm):
    title = StringField(label="Cake Flavor Title  ",validators=[DataRequired(),Length(min=4,max=50)])
    submit = SubmitField("Save")

class CakesForm(FlaskForm):
    title = StringField(label="Cake Title  ",validators=[DataRequired(),Length(min=4,max=50)])
    price = DecimalField(label="Cake Price", validators=[DataRequired()])
    ctype = SelectField(label="Cake Type", validators=[DataRequired()]) #coerce=int,
    csize = SelectField(label="Cake Size", validators=[DataRequired()])
    cflavor = SelectField(label="Cake Flavor",validators=[DataRequired()])
    status = SelectField(label="Cake Status",choices=[('Active', 'Active'), ('In-Active', 'In-Active')],validators=[DataRequired()])
    details  = TextAreaField('Details')
    submit = SubmitField("Save")