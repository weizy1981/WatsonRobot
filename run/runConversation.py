from app.controller.watsonLanguage import WatsonConversation

conversation = WatsonConversation()
#print(conversation.listIntents())
conversation.addExample(intentName='name', question='what is your name')

#dialog_node = conversation.createDailogNode(answer='test is a sample', intentName='test')
#conversation.addDailogNode(dialog_node)
#print(conversation.getWorkspace())

