from app.model import getCollection

class AdminUserModel:

    __collectionName = 'adminuser_collection'

    def insert(self, adminuser):
        adminuser_collection = getCollection(collectionName=self.__collectionName)
        adminuser_collection.insert(adminuser)

    def find(self, username=None):
        adminuser_collection = getCollection(collectionName=self.__collectionName)
        if None == username :
            return adminuser_collection.find()
        else :
            query_key = {'username' : username}
            return adminuser_collection.find_one(query_key)

    def update(self, adminuser):
        adminuser_collection = getCollection(collectionName=self.__collectionName)
        username = adminuser['username']
        password = adminuser['password']
        adminuser_collection.update({'username' : username}, {'$set' : {'password' : password}})

    def delete(self, username):
        adminuser_collection = getCollection(collectionName=self.__collectionName)
        adminuser = self.find(username=username)
        adminuser_collection.delete_one(adminuser)

'''adminUser = AdminUserModel()
user = {'username':'ISSC1228', 'password':'zaq12wsx'}
adminUser.insert(adminuser=user)

users = adminUser.find(username='ISSC1228')
print(users)'''
