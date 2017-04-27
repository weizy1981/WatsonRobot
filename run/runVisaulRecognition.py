from app.controller.watsonVision import WatsonVisaulRecognition

app = WatsonVisaulRecognition()
#positiveFileName = '/Users/wzy/Documents/Watson+Python/visual/cats.zip'
#negativeFileName = '/Users/wzy/Documents/Watson+Python/visual/husky.zip'
#print(app.createClassifier(positive_examples_file=positiveFileName, negative_examples_file=negativeFileName))

#app.createCollection(collectionName='WTASON_ROBOT_VISUAL')
print(app.visaulRecognition.list_images(app.getCollectionId('WTASON_ROBOT_VISUAL')))
