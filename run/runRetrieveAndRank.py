from app.controller.watsonLanguage import WatsonRetrieveAndRank
app = WatsonRetrieveAndRank()
answer = app.doSerach(question='bananas')