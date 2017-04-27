from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired
from app.view import errormessage

class LoginForm(FlaskForm):
    username = StringField(label='username', validators=[DataRequired(errormessage.LOGIN002)])
    password = PasswordField(label='password', validators=[DataRequired(errormessage.LOGIN003)])
    submit = SubmitField(label='GO')

class FileForm(FlaskForm):
    file = FileField(label='File')
    submit = SubmitField(label='GO')

class QuestionForm(FlaskForm):
    question = StringField(label='Question', validators=[DataRequired(errormessage.ONLINE_SERVICE001)])
    submit = SubmitField(label='GO')

class QuerySNForm(FlaskForm):
    customer_id = StringField(label='Customer_Id', validators=[DataRequired(errormessage.QUERY_SN001)])
    submit = SubmitField(label='GO')
    action = ''

class CustomerForm(FlaskForm):
    customer_id = StringField(label='Customer_Id', validators=[DataRequired(errormessage.CUSTOMER_INPUT001)])
    name = StringField(label='Name', validators=[DataRequired(errormessage.CUSTOMER_INPUT002)])
    age = StringField(label='Age', validators=[DataRequired(errormessage.CUSTOMER_INPUT003)])
    sex = StringField(label='Sex', validators=[DataRequired(errormessage.CUSTOMER_INPUT004)])
    submit = SubmitField(label='GO')
    action = ''
