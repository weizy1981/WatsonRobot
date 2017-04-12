from app.controller.watsonLanguage import WatsonToneAnalyzer
app = WatsonToneAnalyzer()
print(app.doAnalyze(text='I am very happy'))