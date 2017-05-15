from app import application
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from werkzeug.utils import secure_filename
from app.model.customer import CustomerModel
from app.model.adminuser import AdminUserModel
from app.view.forms import LoginForm, FileForm, QuestionForm, QuerySNForm, CustomerForm
from app.view import errormessage
from os.path import join
from bson.binary import Binary
from io import BytesIO
from os import remove
from time import time
from app.controller.watsonVision import WatsonVisaulRecognition
from app.controller.watsonLanguage import WatsonDocumentConversion
from app.controller.watsonSpeech import WatsonText2Speech
from app import conversation
from app.controller.customer import getCustomerInfo

@application.route('/')
def index():
    try:
        conversationList = session['conversations']
    except:
        conversationList = None

    audio_file = ''
    if None == conversationList:
        res = conversation.doConversation(questionMsg='Hello')
        conversationList = []
        answer = {}
        answer['text'] = res[0]
        answer['align'] = 'left'
        conversationList.append(answer)
        fileName = str(time()) + '.wav'
        audio_file = join(application.config['UPLOAD_FOLDER'], fileName)
        text2speech = WatsonText2Speech()
        text2speech.text2speech(fileName=audio_file, message=answer['text'])
        audio_file = 'static/resource/' + fileName
    session['conversations'] = conversationList
    form = QuestionForm()
    return render_template('customerservice.html',
                           conversationList=conversationList,
                           form=form, audio_file=audio_file)


@application.route('/doconversation', methods=['POST'])
def doConversation():
    conversationList = session['conversations']
    form = QuestionForm()
    if form.validate_on_submit():

        msg = form.question.data
        question = {'text': msg, 'align': 'right'}
        conversationList.append(question)

        res = conversation.doConversation(questionMsg=msg)
        answer = {'text': res[0], 'align': 'left'}
        conversationList.append(answer)

        fileName = str(time()) + '.wav'
        audio_file = join(application.config['UPLOAD_FOLDER'], fileName)
        text2speech = WatsonText2Speech()
        text2speech.text2speech(fileName=audio_file, message=answer['text'])
        audio_file = 'static/resource/' + fileName

        session['conversations'] = conversationList
        form.question.data = ''
        return render_template('customerservice.html',
                               conversationList=conversationList,
                               form=form,
                               audio_file=audio_file)
    else:
        return render_template('customerservice.html',
                               conversationList=conversationList,
                               form=form)


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
            #return redirect('/customerlist')
            return customerList()
        else:
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
    form = FileForm()
    form.action = 'douploadimg'
    if request.method == 'GET':
        try:
            customer_id = request.args['customer_id']
        except:
            customer_id = ''
        session['customer_id'] = customer_id
    return render_template('uploadimg.html', form=form)


@application.route('/douploadimg', methods=['POST', 'GET'])
def douploadimg():
    form = FileForm()
    form.action = 'douploadimg'

    if form.validate_on_submit():
        customer_id = session['customer_id']
        file = form.file.data

        # 保存上传的文件到临时文件
        fileName = str(time()) + secure_filename(file.filename)
        path = join(application.config['UPLOAD_FOLDER'], fileName)
        file.save(path)

        # 获取customer
        customerModel = CustomerModel()
        customer = customerModel.find(customer_id=customer_id)

        if None != customer:
            with open(path, 'rb') as myImage:
                # Training Watson Visaul
                watsonVision = WatsonVisaulRecognition()
                # 删除现存的Training图片
                if 'watson_images' in customer['customer_info']:
                    for image_id in customer['customer_info']['watson_images']:
                        try:
                            watsonVision.deleteImageFromCollection(
                                collectionName=application.config['WTASON_ROBOT_VISUAL_COLLECTION'],
                                image_id=image_id)
                        except:
                            print('%s is not found' % image_id)
                # 删除MongoDB中的图片信息
                if 'customer_image' in customer['customer_info']:
                    del (customer['customer_info']['customer_image'])
                if 'watson_images' in customer['customer_info']:
                    del (customer['customer_info']['watson_images'])

                # 重新Training Watson
                res = watsonVision.addImageToCollection(
                    collectionName=application.config['WTASON_ROBOT_VISUAL_COLLECTION'],
                    image=myImage,
                    metadata=customer['customer_info'])

                # 保存Training watson的结果信息到customer，准备保存相关信息到Mongo DB
                watson_images = res['images']
                customerImages = []
                for image in watson_images:
                    image_id = image['image_id']
                    customerImages.append(image_id)
                customer['customer_info']['watson_images'] = customerImages

                # 保存上传的文件到MongoDB
                imageContent = BytesIO(myImage.read())
                customer_image = {}
                customer_image['image'] = Binary(imageContent.getvalue())
                customer_image['filename'] = fileName
                customer['customer_info']['customer_image'] = customer_image
                customerModel.update(customer=customer)

        # 删除临时文件
        remove(path)

        session.pop('customer_id', None)
        return redirect('/customerlist')

    else:
        return render_template('uploadimg.html', form=form)


@application.route('/showcustomerinfo', methods=['GET'])
def showCustomerInfo():
    if request.method == 'GET':

        customer_id = request.args['customer_id']
        customer_info_list = getCustomerInfo(customer_id=customer_id)
        return render_template('customerinfo.html', customer_info_list=customer_info_list)
    else:
        return redirect('/customerlist')


@application.route('/goquerysn')
def goQuerySN():
    form = QuerySNForm()
    return render_template('querysn.html', form=form)


@application.route('/doquerysn', methods=["POST"])
def doQuerySN():
    form = QuerySNForm()
    if form.validate_on_submit():
        customer_id = form.customer_id.data
        customer_info_list = getCustomerInfo(customer_id=customer_id)
        return render_template('customerinfo.html', customer_info_list=customer_info_list)
    else:
        return render_template('querysn.html', form=form)


@application.route('/govisaulquery')
def goVisualQuery():
    form = FileForm()
    form.action = 'dovisualquery'
    return render_template('uploadimg.html', form=form)


@application.route('/dovisualquery', methods=['POST'])
def doVisualQuery():
    form = FileForm()
    form.action = 'dovisualquery'
    if form.validate_on_submit():
        file = form.file.data

        # 保存上传的文件到临时文件
        fileName = str(time()) + secure_filename(file.filename)
        path = join(application.config['UPLOAD_FOLDER'], fileName)
        file.save(path)

        watsonVision = WatsonVisaulRecognition()
        res = watsonVision.getSimilar(collectionName=application.config['WTASON_ROBOT_VISUAL_COLLECTION'], image=path)
        customer_id = res['similar_images'][0]['metadata']['customer_id']
        customer_info_list = getCustomerInfo(customer_id=customer_id)
        remove(path)
        return render_template('customerinfo.html', customer_info_list=customer_info_list)
    else:
        return render_template('uploadimg.html', form=form)


@application.route('/gocustomerbyinput')
def goCustomerByInput():
    form = CustomerForm()
    form.action = 'docustomerbyinput'
    return render_template('customerinput.html', form=form)


@application.route('/docustomerbyinput', methods=['POST'])
def doCustomerByInput():
    form = CustomerForm()
    form.action = 'docustomerbyinput'
    if form.validate_on_submit():
        customer_id = form.customer_id.data
        name = form.name.data
        age = form.age.data
        sex = form.sex.data
        customer_info = {'customer_id': customer_id, 'name': name, 'age': age, 'sex': sex}
        customer = {'customer_id': customer_id, 'customer_info': customer_info}
        customer_db = CustomerModel()
        try:
            customer_db.insert(customer=customer)
            return redirect('/customerlist')
        except:
            return render_template('customerinput.html', form=form, error=errormessage.CUSTOMER_INPUT005)
    else:
        return render_template('customerinput.html', form=form)


@application.route('/gocustomerfromcsv')
def goCustomerFromCSV():
    form = FileForm()
    form.action = 'docustomerfromcsv'
    return render_template('uploadimg.html', form=form)


@application.route('/gocustomerfromword')
def goCustomerFromWord():
    form = FileForm()
    form.action = 'docustomerfromword'
    return render_template('uploadimg.html', form=form)


@application.route('/gocustomerfromimg')
def goCustomerFromImg():
    form = FileForm()
    form.action = 'docustomerfromimg'
    return render_template('uploadimg.html', form=form)


@application.route('/gocustomerfrompdf')
def goCustomerFromPDF():
    form = FileForm()
    form.action = 'docustomerfrompdf'
    return render_template('uploadimg.html', form=form)

@application.route('/docustomerfromcsv', methods=['POST'])
def doCustomerFromCSV():
    form = FileForm()
    form.action = 'docustomerfromcsv'
    if form.validate_on_submit():
        file = form.file.data

        # 保存上传的文件到临时文件
        fileName = str(time()) + secure_filename(file.filename)
        path = join(application.config['UPLOAD_FOLDER'], fileName)
        file.save(path)

        with open(path, 'r') as mycsv:
            valueList = mycsv.readlines()
            keyList = list(valueList[0].split(','))
            valueList.pop(0)
            customerDB = CustomerModel()
            for value in valueList:
                values = list(value.split(','))
                customer = {'customer_id': values[0]}
                customer_info = {}
                for i in range(1, len(keyList) - 1):
                    customer_info[keyList[i]] = values[i]
                customer['customer_info'] = customer_info
                customerDB.insert(customer=customer)

        remove(path)
        return redirect('/customerlist')
    else:
        return render_template('uploadimg.html', form=form)

@application.route('/docustomerfromword', methods=['POST'])
def doCustomerFromWord():
    form = FileForm()
    form.action = 'docustomerfromword'
    if form.validate_on_submit():
        file = form.file.data

        # 保存上传的文件到临时文件
        fileName = str(time()) + secure_filename(file.filename)
        path = join(application.config['UPLOAD_FOLDER'], fileName)
        file.save(path)

        documentConversion = WatsonDocumentConversion()
        '''config = {'conversion_target': 'answer_units',
                  'word': {
                      'heading': {
                          'fonts': [
                              {'level': 1, 'min_size': 8, 'max_size': 12}
                          ]
                      }
                  }
                  }'''
        res = documentConversion.doDocumentConversion(fileName=path)
        print(res)

        return redirect('/customerlist')
    else:
        return render_template('uploadimg.html', form=form)

@application.route('/uploadquestion')
def goUploadQuestion():
    form = FileForm()
    form.action = 'douploadquestion'
    return render_template('uploadimg.html', form=form)

@application.route('/douploadquestion', methods=['POST'])
def doUploadQuestion():
    form = FileForm()
    form.action = 'douploadquestion'
    if form.validate_on_submit():
        file = form.file.data

        # 保存上传的文件到临时文件
        fileName = str(time()) + secure_filename(file.filename)
        path = join(application.config['UPLOAD_FOLDER'], fileName)
        file.save(path)

        with open(path, 'r') as mycsv:
            valueList = mycsv.readlines()
            valueList.pop(0)

            for value in valueList:
                values = list(value.split(','))
                conversation.addExample(intentName=values[0], question=values[1].strip())

        remove(path)
        return redirect('/customerlist')
    else:
        return render_template('uploadimg.html', form=form)

@application.route('/uploadanswer')
def goUploadAnswer():
    form = FileForm()
    form.action = 'douploadanswer'
    return render_template('uploadimg.html', form=form)

@application.route('/douploadanswer', methods=['POST'])
def doUploadAnswer():
    form = FileForm()
    form.action = 'douploadanswer'
    if form.validate_on_submit():
        file = form.file.data

        # 保存上传的文件到临时文件
        fileName = str(time()) + secure_filename(file.filename)
        path = join(application.config['UPLOAD_FOLDER'], fileName)
        file.save(path)

        with open(path, 'r') as mycsv:
            valueList = mycsv.readlines()
            valueList.pop(0)

            for value in valueList:
                values = list(value.split(','))
                dialog_node = conversation.createDailogNode(intentName=values[0], answer=values[1].strip())
                conversation.addDailogNode(dialog_node)

        remove(path)
        return redirect('/customerlist')
    else:
        return render_template('uploadimg.html', form=form)
