import pymongo
import ssl

MONGODB_URL = 'mongodb://admin:GGGRCAPOQYDGTXMN@bluemix-sandbox-dal-9-portal.7.dblayer.com:26175,bluemix-sandbox-dal-9-portal.6.dblayer.com:26175/admin?ssl=true'

client = pymongo.MongoClient(MONGODB_URL, ssl_cert_reqs=ssl.CERT_NONE)
db = client.get_default_database()
print(db.collection_names())
