from app.model import getCollection


class CustomerModel:
    __collectionName = 'customer_collection'
    def insert(self, customer):
        customer_collection = getCollection(collectionName=self.__collectionName)
        customer_collection.insert(customer)

    def find(self, customer_id=None):
        customer_collection = getCollection(collectionName=self.__collectionName)
        if None == customer_id:
            customers = customer_collection.find()
            return customers
        else:
            query_key = {'customer_id': customer_id}
            customer = customer_collection.find_one(query_key)
            return customer

    def update(self, customer):
        customer_collection = getCollection(collectionName=self.__collectionName)

        customer_id = customer['customer_id']
        customer_info = customer['customer_info']

        customer_collection.update({'customer_id': customer_id}, {'$set': {'customer_info': customer_info}})

    def delete(self, customer_id):
        customer_collection = getCollection(collectionName=self.__collectionName)
        customer = self.find(customer_id=customer_id)
        customer_collection.delete_one(customer)

'''customer = CustomerModel()
#wzy = {'customer_id' : 'ISSC1228', 'customer_info' : {'name' : 'wzy', 'age' : '36', 'sex' : 'M'}}
customers = customer.find()
for customer in customers:
    print(customer)'''
