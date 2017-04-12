from watson_developer_cloud import ConversationV1
from watson_developer_cloud import NaturalLanguageClassifierV1
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding.features import v1 as features
from watson_developer_cloud import LanguageTranslatorV2
from watson_developer_cloud import PersonalityInsightsV3
from watson_developer_cloud import DocumentConversionV1
from watson_developer_cloud import RetrieveAndRankV1
from watson_developer_cloud import ToneAnalyzerV3


class WatsonConversation:
    # 定义conversation对象
    conversation = None
    # 调用 conversation 的参数
    username = 'ba1fbe43-ba2d-40e6-8e01-f2fe8a2e77c1'
    password = 'RVmKhhzt7oQY'
    version = '2017-02-03'
    workspace_id = 'a52b6296-7de3-46c0-8445-f7ab3337678b'
    context = None

    # 类的初始化函数
    def __init__(self):
        # print('this is watson conversation start')
        self.conversation = ConversationV1(username=self.username, password=self.password, version=self.version)

    # 对话功能的实现
    def doConversation(self, questionMsg=''):
        # 调用conversation的message得到输入的反馈结果
        response = self.conversation.message(workspace_id=self.workspace_id, message_input={
            'text': questionMsg}, context=self.context)
        # 返回的结果
        output = response['output']
        # 保存对话的context，为下次调用维持在同一个Dialog中
        self.context = response['context']
        # 返回这次的回答
        answerMsg = output['text']
        return answerMsg


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

    def doDocumentConversion(self, fileName, media_type=None):
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
