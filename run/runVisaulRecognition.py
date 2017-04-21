from app.controller.watsonVision import WatsonVisaulRecognition

app = WatsonVisaulRecognition()
#positiveFileName = '/Users/wzy/Documents/Watson+Python/visual/cats.zip'
#negativeFileName = '/Users/wzy/Documents/Watson+Python/visual/husky.zip'
#print(app.createClassifier(positive_examples_file=positiveFileName, negative_examples_file=negativeFileName))
image = '/Users/wzy/Documents/Watson+Python/visual/wei.jpg'

print(app.detectFace(image=image))