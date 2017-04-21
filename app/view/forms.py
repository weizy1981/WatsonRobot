from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired
from app.view import errormessage

fileAllowedSet = set(['jpg', 'jpeg', 'png', 'gif'])
class LoginForm(FlaskForm):
    username = StringField(label='username', validators=[DataRequired(errormessage.LOGIN002)])
    password = PasswordField(label='password', validators=[DataRequired(errormessage.LOGIN003)])
    submit = SubmitField('GO')


class PhotoForm(FlaskForm):
    photo = FileField(label='Photo', validators=[FileRequired(errormessage.UPLOAD001),
                                  FileAllowed(fileAllowedSet, errormessage.UPLOAD002)])

    submit = SubmitField('GO')
