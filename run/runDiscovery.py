from app.controller.watsonDataInsight import WatsonDiscovery
app = WatsonDiscovery()
print(app.doQuery('IBM'))