from app.apl import dialog
from app.controller.watsonLanguage import WatsonLanguageTranslator
from app.controller.watsonLanguage import WatsonPersonalityInsight

def printMsg(message='') :
    msgList = dialog(message=message)
    for msg in msgList :
        print(msg)

printMsg()

while True :
    inputMsg = input()
    printMsg(message=inputMsg)


'''text = 'Analyze text to extract meta-data from content such as concepts, entities, keywords, categories, sentiment, ' \
       'emotion, relations, semantic roles, using natural language understanding. With custom annotation models ' \
       'developed using Watson Knowledge Studio, identify industry/domain specific entities and relations in ' \
       'unstructured text.'

#languageTranslator = WatsonLanguageTranslator()
#print(languageTranslator.translate(text='Hello, who are you?', target='fr'))

personalityInsight = WatsonPersonalityInsight()
text = "Okposo played one season in the United States Hockey League (USHL) with the Des Moines Buccaneers in " \
       "which he was named the most valuable player of the USHL playoffs and the league's top rookie. " \
       "He helped the Buccaneers to a Clark Cup victory. During his freshman season at University of Minnesota, " \
       'Okposo was placed at the center position, even though he is a natural winger. ' \
       'Throughout most of the season this became his most common position due to the abundance of wingers on the team. ' \
       'In January 2007, he played for the U.S. National Junior Team in the 2007 IIHF World Junior Championship. ' \
       'On June 7, 2007, Okposo announced he would be returning to the University of Minnesota for the 2007–08 season. ' \
       'Okposo played the 2007–08 season for the University of Minnesota ice hockey team until December 19, 2007. ' \
       'On that morning Okposo notified his teammates at the university of his decision to leave the team. Soon after, ' \
       'both the Gophers and the New York Islanders announced officially ' \
       'that Okposo decided to leave college after the completion of his current semester ' \
       'and would then begin his professional hockey career.'
print(personalityInsight.getProfile(text=text, language='en'))'''
