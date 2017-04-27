from app.model.customer import CustomerModel
def getCustomerInfo(customer_id):
    customer = CustomerModel().find(customer_id=customer_id)
    customer_info = customer['customer_info']
    customer_info_list = []
    for key in customer_info:
        if isinstance(customer_info[key], str):
            label = key + ' : ' + customer_info[key]
            customer_info_list.append(label)
    return customer_info_list

