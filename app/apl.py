from app.controller.watsonLanguage import WatsonConversation
from app.controller.watsonLanguage import WatsonLanguageClassifier

conversation = WatsonConversation()
classifier = WatsonLanguageClassifier()

def dialog(message='') :
    returnValue = ''

    classifierResult = ''
    if message != '' :
        classifierResult = classifier.classifier(text=message)

    if classifierResult == '' :
        returnValue = conversation.doConversation(questionMsg=message)
    elif classifierResult == 'temperature' :
        returnValue = ['30F']
    elif classifierResult == 'conditions' :
        returnValue = ['Yes']
    return returnValue