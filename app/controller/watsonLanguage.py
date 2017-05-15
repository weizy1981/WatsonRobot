from watson_developer_cloud import ConversationV1
from watson_developer_cloud import NaturalLanguageClassifierV1
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding.features import v1 as features
from watson_developer_cloud import LanguageTranslatorV2
from watson_developer_cloud import PersonalityInsightsV3
from watson_developer_cloud import DocumentConversionV1
from watson_developer_cloud import RetrieveAndRankV1
from watson_developer_cloud import ToneAnalyzerV3
from time import time


class WatsonConversation:
    # 定义conversation对象
    conversation = None
    # 调用 conversation 的参数
    username = 'ba1fbe43-ba2d-40e6-8e01-f2fe8a2e77c1'
    password = 'RVmKhhzt7oQY'
    version = '2017-04-21'
    workspace_id = 'a52b6296-7de3-46c0-8445-f7ab3337678b'
    context = None

    # 类的初始化函数
    def __init__(self):
        # print('this is watson conversation start')
        self.conversation = ConversationV1(username=self.username, password=self.password, version=self.version)

    def getWorkspace(self):
        res = self.conversation.get_workspace(workspace_id=self.workspace_id, export=True)
        return res

    def getDialogNodes(self):
        res = self.getWorkspace()
        return res['dialog_nodes']

    def hasDialogNode(self, dialog_node):
        result = False
        for tmpDialogNode in self.getDialogNodes() :
            if dialog_node['dialog_node'] == tmpDialogNode['dialog_node'] :
                result = True
                break;
        return result

    def getLastDialogNode(self):
        res = self.getDialogNodes()
        #print(res)
        length = len(res)
        if length == 0 :
            return None
        else :
            return res[length - 1]

    def getLastDialogNodeName(self):
        try :
            res = self.getLastDialogNode()
            return res['dialog_node']
        except :
            return None

    def createDailogNode(self, answer, intentName):
        res = {}
        res['output'] = {'text': {'values': [answer], 'selection_policy': 'sequential'}}
        res['dialog_node'] = intentName
        res['previous_sibling'] = self.getLastDialogNodeName()
        res['conditions'] = '#' + intentName
        return res

    def makeDailogNodes(self):
        dialog_nodes = []
        tmpList = self.getDialogNodes()
        for dialog_node in tmpList:
            dialog_nodes.append(self.makeDialogNode(dialogNode=dialog_node))
        return dialog_nodes

    def makeDialogNode(self, dialogNode):
        res = {}
        res['output'] = dialogNode['output']
        res['dialog_node'] = dialogNode['dialog_node']
        res['previous_sibling'] = dialogNode['previous_sibling']
        res['conditions'] = dialogNode['conditions']
        return res


    def addDailogNode(self, dialog_node = None):
        dialog_nodes = self.makeDailogNodes()
        if None != dialog_node :
            if not self.hasDialogNode(dialog_node=dialog_node) :
                for dialog_node_tmp in dialog_nodes:
                    if dialog_node_tmp ['previous_sibling'] == self.getLastDialogNodeName() :
                        dialog_node_tmp['previous_sibling'] = dialog_node['dialog_node']
                        break
                dialog_nodes.append(dialog_node)
        #print(dialog_nodes)
        return self.conversation.update_workspace(workspace_id=self.workspace_id, dialog_nodes=dialog_nodes)



    # 对话功能的实现
    def doConversation(self, questionMsg=''):
        # 调用conversation的message得到输入的反馈结果
        response = self.conversation.message(workspace_id=self.workspace_id, message_input={'text': questionMsg}, context=self.context)
        # 返回的结果
        output = response['output']
        # 保存对话的context，为下次调用维持在同一个Dialog中
        self.context = response['context']
        # 返回这次的回答
        answerMsg = output['text']
        return answerMsg

    def listIntents(self):
        params = {'version': self.version}
        params['export'] = None
        params['page_limit'] = None
        params['include_count'] = None
        params['sort'] = None
        params['cursor'] = None
        res = self.conversation.request(
            method='GET',
            url='/v1/workspaces/{0}/intents'.format(self.workspace_id),
            params=params,
            accept_json=True)
        return res
        #print(res)

    def __getIntent(self, intentName):
        res = self.listIntents()
        intentList = res['intents']
        value = None
        for intent in intentList :
            if intentName == intent['intent']:
                value = intent
                break
        return value

    def addExample(self, intentName, question):
        intent = self.__getIntent(intentName=intentName)

        if None == intent :
            self.__create_intent(intent=intentName, description=intentName)

        try :
            self.__create_example(intentName=intentName, text=question)
        except Exception as e:
            print(e)


    def __create_intent(self,
                      intent,
                      description=None,
                      examples=None):
        """
        Create intent.
        :param workspace_id: The workspace ID.
        :param intent: The name of the intent.
        :param description: The description of the intent.
        :param examples: An array of user input examples.
        """
        params = {'version': self.version}
        data = {}
        data['intent'] = intent
        data['description'] = description
        data['examples'] = examples
        return self.conversation.request(
            method='POST',
            url='/v1/workspaces/{0}/intents'.format(self.workspace_id),
            params=params,
            json=data,
            accept_json=True)

    def __create_example(self, intentName, text):
        """
        Create user input example.
        :param workspace_id: The workspace ID.
        :param intentName: The intent name (for example, `pizza_order`).
        :param text: The text of a user input example.
        """
        params = {'version': self.version}
        data = {}
        data['text'] = text
        return self.conversation.request(
            method='POST',
            url='/v1/workspaces/{0}/intents/{1}/examples'.format(
                self.workspace_id, intentName),
            params=params,
            json=data,
            accept_json=True)


class WatsonLanguageClassifier:
    languageClassifier = None
    username = 'b50574a3-8edd-4a46-a2de-e54d4cfaec91'
    password = '0MbpaBuEPwdv'
    classifier_id = '90e7b7x198-nlc-28066'
    confidenceLimit = 0.95

    # 类的初始化函数
    def __init__(self):
        # print('this is watson Language Classifiter  start')
        self.languageClassifier = NaturalLanguageClassifierV1(username=self.username, password=self.password)

        # 列出当前service中存在的所有classifiter
        # classifiterList = self.languageClassifiter.list()

    # 创建classifiter并训练
    def createClassifier(self, fileName=''):
        if fileName == '':
            fileName = '/Users/wzy/Downloads/weather_data_train.csv'
        with open(fileName, 'rb') as trainingData:
            classifiter = self.languageClassifier.create(training_data=trainingData, name='my classifiter')

    # 获取分词类别
    def classifier(self, text):
        myClassifierResults = self.languageClassifier.classify(classifier_id=self.classifier_id, text=text)
        confidence = myClassifierResults['classes'][0]['confidence']

        returnValue = ''
        if confidence > self.confidenceLimit:
            returnValue = myClassifierResults['top_class']

        return returnValue


class WatsonLanguageUnderstanding:
    languageUnderstanding = None
    username = '4c0e2d8d-10ed-4192-8605-a740bde5b586'
    password = 'HQBlipDb4vIl'
    version = '2017-02-27'

    # 类的初始化函数
    def __init__(self):
        self.languageUnderstanding = NaturalLanguageUnderstandingV1(username=self.username, password=self.password,
                                                                    version=self.version)

    def analyze(self, text=None):
        # 定义语言分析的方面
        featuresTarget = [features.Categories(), features.Concepts(),
                          features.Emotion(), features.Entities(),
                          features.Keywords()]
        if text != None:
            response = self.languageUnderstanding.analyze(text=text, features=featuresTarget)
            return response


class WatsonLanguageTranslator:
    languageTranslator = None
    username = 'bffc36ec-3515-42e2-a68e-3564b1af2ceb'
    password = 'DZbmbAE5F0re'

    def __init__(self):
        self.languageTranslator = LanguageTranslatorV2(username=self.username, password=self.password)
        # 能够识别的语言种类
        # self.languageTranslator.get_identifiable_languages()

    def translate(self, text, target='en'):
        # 识别输入语言的语种
        languageType = self.languageTranslator.identify(text=text)['languages'][0]['language'][:2]
        # 翻译成为目标语言
        response = self.languageTranslator.translate(text=text, source=languageType, target=target)
        return response


class WatsonPersonalityInsight:
    personalityInsight = None
    username = '845490e8-8f94-4766-a41f-47d0a6e39f4a'
    password = '4STBAVK1BJUT'
    version = '2016-10-20'

    def __init__(self):
        self.personalityInsight = PersonalityInsightsV3(username=self.username, password=self.password,
                                                        version=self.version)

    def getProfile(self, text, language='ja'):
        # content_type = 'text/plan' or 'text/html' or 'application/json'
        # accept = 'application/json'(default) or 'text/csv'
        response = self.personalityInsight.profile(text=text.encode('utf-8'),
                                                   content_type='text/plain',
                                                   content_language=language,
                                                   accept_language=language,
                                                   accept='application/json',
                                                   raw_scores=True,
                                                   consumption_preferences=True)
        return response


class WatsonDocumentConversion:
    documentConversation = None
    username = '0dab19d1-cbba-4705-a1f3-eedf01fee78d'
    password = 'UI1xdpFjwVPL'
    version = '2015-12-15'

    def __init__(self):
        self.documentConversation = DocumentConversionV1(username=self.username,
                                                         password=self.password,
                                                         version=self.version)

    def doDocumentConversion(self, fileName, config=None, media_type=None):
        if None == config :
            config = {'conversion_target': DocumentConversionV1.ANSWER_UNITS}

        with open(fileName, 'r') as document:
            response = self.documentConversation.convert_document(document=document,
                                                                  config=config,
                                                                  media_type=media_type)
            return response


class WatsonRetrieveAndRank:
    retrieveAndRank = None
    username = '4ca5cb7e-0873-44b8-8823-7b8a9466e840'
    password = '5Trau3u4oH6j'
    cluster_id = 'scf8e8a5f1_eb8a_4754_8274_91bafcb38dca'

    def __init__(self):
        self.retrieveAndRank = RetrieveAndRankV1(username=self.username, password=self.password)
        # 查看retrieve and rank service中存在的cluster
        # print(self.retrieveAndRank.list_solr_clusters())
        # 查看指定cluster中存在的collections
        # print(self.retrieveAndRank.list_collections(solr_cluster_id=self.cluster_id))
        # 查看指定cluster的configs
        # print(self.retrieveAndRank.list_configs(solr_cluster_id=self.cluster_id))

    def doSerach(self, question=''):
        # 查看指定cluster中存在的collections
        collections = self.retrieveAndRank.list_collections(solr_cluster_id=self.cluster_id)

        pysolr_client = self.retrieveAndRank.get_pysolr_client(solr_cluster_id=self.cluster_id,
                                               collection_name=collections['collections'][0])

        result = pysolr_client.search(q=question)
        return result

class WatsonToneAnalyzer:

    toneAnalyzer = None
    username = '63bc1c45-ebba-45e3-bb40-30d384260e64'
    password = '8qT3TkgGCgyL'
    version = '2016-05-19'

    def __init__(self):
        self.toneAnalyzer = ToneAnalyzerV3(username=self.username, password=self.password, version=self.version)

    def doAnalyze(self, text):
        response = self.toneAnalyzer.tone(text=text)
        return response
