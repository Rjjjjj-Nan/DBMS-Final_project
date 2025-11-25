from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField (
        "Sr-Code",
        validators=[DataRequired()]
    )

    password = PasswordField (
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    name = StringField (
        "Name",
        validators=[DataRequired()]
    )

    surname = StringField (
        "Surname",
        validators=[DataRequired()]
    )

    age = IntegerField (
        "Age",
        validators=[DataRequired()]
    )

    sr_code = StringField (
        "Sr-Code",
        validators=[DataRequired()]
    )

    email = StringField (
        "Email",
        validators=[DataRequired()]
    )

    contact_number = StringField (
        "Contact",
        validators=[DataRequired()]
    )

    gender = SelectField (
        "Sex",
        choices = ['male', 'female'],
        validators=[DataRequired()]
    )

    username = StringField (
        "Username",
        validators=[DataRequired()]
    )

    password = StringField (
        "Password",
        validators=[DataRequired()]
    )

    role = SelectField (
        "Role",
        choices = ['student', 'admin'],
        validators=[DataRequired()]
    )

    submit = SubmitField("Submit")

class ReportForm(FlaskForm):
    item = StringField (
        "Item",
        validators=[DataRequired()]
    )

    place = StringField (
        "Place",
        validators=[DataRequired()]
    )

    photo = FileField (
        "Upload Picture",
        validators=[
            DataRequired(), 
            FileAllowed(['jpg', 'png', 'jpeg'], 'Images Only!')
        ]
    )

    description = StringField (
        "Description",
        validators=[DataRequired()]
    )

    submit = SubmitField("Submit")

class ReturnForm(FlaskForm):
    item_id = IntegerField(
        "Item ID",
        validators=[DataRequired()]
    )

    name = StringField (
        "Owner Name",
        validators=[DataRequired()]
    )

    email = StringField (
        "Email",
        validators=[DataRequired()]
    )

    contact = StringField (
        "Contact",
        validators=[DataRequired()]
    )

    submit = SubmitField("Submit")