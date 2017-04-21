from app import application
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from werkzeug.utils import secure_filename
from app.model.customer import CustomerModel
from app.model.adminuser import AdminUserModel
from app.view.forms import LoginForm, PhotoForm
from app.view import errormessage
from werkzeug.datastructures import CombinedMultiDict


@application.route('/')
def index():
    return render_template('customerservice.html')

@application.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@application.route('/dologin', methods=['POST'])
def dologin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        admin = AdminUserModel()
        adminuser = admin.find(username=username)

        if None != adminuser and password == adminuser['password']:
            return redirect('/customerlist')
        else :
            return render_template('login.html', form=form, error=errormessage.LOGIN001)
    else:
        return render_template('login.html', form=form)

@application.route('/customerlist')
def customerList():
    customerModel = CustomerModel()
    customerList = customerModel.find()
    return render_template('customerlist.html', customerList=customerList)


@application.route('/uploadimg', methods=['GET'])
def uploadimg():
    form = PhotoForm()
    if request.method == 'GET':
        try:
            customer_id = request.args['customer_id']
        except :
            customer_id = ''
        session['customer_id'] = customer_id
    return render_template('uploadimg.html', form=form)

@application.route('/douploadimg', methods=['POST', 'GET'])
def douploadimg():
    #values = CombinedMultiDict([request.files, request.form])
    form = PhotoForm()

    if form.validate_on_submit():
        customer_id = session['customer_id']
        print(customer_id)
        file = form.photo.data
        print(file)
        #fileName = secure_filename(file.filename)
    
        session.pop('customer_id', None)
        return redirect('/customerlist')
    else :
        return render_template('uploadimg.html', form=form)

