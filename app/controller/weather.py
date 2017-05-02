from watson_developer_cloud import WatsonDeveloperCloudService

class Weather(WatsonDeveloperCloudService):

    default_url = 'https://twcservice.mybluemix.net:443/api/weather/'
    api_url = 'v1/geocode/45.42/75.69/forecast/hourly/48hour.json'

    def __init__(self, username=None, password=None, api_url=None, language='en-US', params = None,
                 use_vcap_services=True):

        if None != api_url :
            self.api_url = api_url

        queryParam = {'language' : language}
        if params != None :
            queryParam.update(params)

        self.api_url = self.api_url + self.__makeQueryParams(params=queryParam)

        WatsonDeveloperCloudService.__init__(
            self, 'weather', self.default_url, username, password, use_vcap_services)

    def getWeather(self):
        return self.request(method='GET',
                            url=self.api_url,
                            accept_json=True)

    def __makeQueryParams(self, params):
        param = '?'
        for key in params :
            param = param + key + '=' + params[key] + '&'
        param = param[0:len(param) - 1]
        return param

