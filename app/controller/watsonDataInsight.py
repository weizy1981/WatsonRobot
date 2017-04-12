from watson_developer_cloud import DiscoveryV1


class WatsonDiscovery:
    discovery = None
    username = 'c7b9c0d4-89fa-446c-acc9-72dd31195c4b'
    password = 'TFInsgGDIdS6'
    version = '2016-12-01'
    environmentId = None
    collectionId = None
    configurationId = None

    def __init__(self):
        self.discovery = DiscoveryV1(username=self.username, password=self.password, version=self.version)
        if None == self.environmentId:
            self.environmentId = self.__getEnvironment(environmentName='Watson News Environment')['environment_id']
        if None == self.collectionId:
            self.collectionId = self.__getCollection(environmentId=self.environmentId,
                                                     collectionName='watson_news')['collection_id']
        if None == self.configurationId:
            configuration = self.__getConfiguration(environmentId=self.environmentId,
                                                    configurationName='Default Configuration')['configuration_id']

    # 获取Discovery的Environment信息
    def __getEnvironment(self, environmentName):
        response = None
        environments = self.discovery.get_environments()
        for environment in environments['environments']:
            if environment['name'] == environmentName:
                response = environment
                break
        return response

    # 获取collection信息
    def __getCollection(self, environmentId, collectionName):
        response = None
        collections = self.discovery.list_collections(environment_id=environmentId)['collections']
        for collection in collections:
            if collection['name'] == collectionName:
                response = collection
                break
        return response

    # 获取Configuration信息
    def __getConfiguration(self, environmentId, configurationName):
        response = None
        configurations = self.discovery.list_configurations(environment_id=environmentId)['configurations']
        for configuration in configurations:
            if configuration['name'] == configurationName:
                response = configuration
                break
        return response

    # 检索获取信息
    def doQuery(self, question):
        query_options = {'query': question}
        queryResult = self.discovery.query(query_options=query_options, environment_id=self.environmentId,
                                           collection_id=self.collectionId)
        return queryResult
