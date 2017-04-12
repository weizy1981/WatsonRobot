from app.controller.watsonLanguage import WatsonDocumentConversion

app = WatsonDocumentConversion()
fileName = '/Users/wzy/Documents/PycharmProjects/WatsonRobot/resource/sample.html'
print(app.doDocumentConversion(fileName=fileName))