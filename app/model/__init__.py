from pymongo import MongoClient
import ssl

# Local MongoDB connection
# mongoURL = 'mongodb://localhost:27017//'
# client = MongoClient(mongoURL)

# Connection to bluemix mongodb
MONGODB_URL = 'mongodb://admin:GGGRCAPOQYDGTXMN@bluemix-sandbox-dal-9-portal.7.dblayer.com:26175,bluemix-sandbox-dal-9-portal.6.dblayer.com:26175/admin?ssl=true'
client = MongoClient(MONGODB_URL, ssl_cert_reqs=ssl.CERT_NONE)

mangodb = client['ccs']


def getCollection(collectionName):
    collection = mangodb[collectionName]
    return collection
