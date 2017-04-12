from watson_developer_cloud import VisualRecognitionV3


class WatsonVisaulRecognition:
    visaulRecognition = None
    api_key = 'ae8ad2f7c599b7962737b7fed7052c34ef1fa137'
    version = '2016-05-20'
    classifier_ids = ['cats_365269959', 'default']

    # 初始化visual recognition
    def __init__(self):
        self.visaulRecognition = VisualRecognitionV3(api_key=self.api_key, version=self.version)

    # 创建classifier
    def createClassifier(self, positive_examples_file, negative_examples_file=None):
        name = 'cats'
        response = None
        if None == negative_examples_file:
            with open(positive_examples_file, 'rb') as positive_examples:
                response = self.visaulRecognition.create_classifier(name=name, cats_positive_examples=positive_examples)
        else:
            with open(positive_examples_file, 'rb') as positive_examples, \
                    open(negative_examples_file, 'rb') as negative_examples:
                response = self.visaulRecognition.create_classifier(name=name, cats_positive_examples=positive_examples,
                                                                    negative_examples=negative_examples)
        return response

    # 创建collection
    def createCollection(self, collectionName):
        return self.visaulRecognition.create_collection(name=collectionName)

    # image : image的path
    # metadata ：dict对象，描述照片的信息metadata = {'name' : 'Name', 'age' : '25', 'cellphone' : 'cellno'}
    def addImageToCollection(self, collectionName, image, metadata=None):
        collectionId = self.__getCollectionId(collectionName=collectionName)
        with open(image, 'rb') as image_file:
            response = self.visaulRecognition.add_image(collection_id=collectionId, image_file=image_file,
                                                        metadata=metadata)
            return response

    # 从自己的collection找到相似的照片返回照片的信息
    def getSimilar(self, collectionName, image):
        collectionId = self.__getCollectionId(collectionName=collectionName)
        with open(image, 'rb') as image_file:
            response = self.visaulRecognition.find_similar(collection_id=collectionId, image_file=image_file)
            return response

    # 根据collection name获取collection id
    def __getCollectionId(self, collectionName):
        collections = self.visaulRecognition.list_collections()['collections']
        collectionId = ''
        for collection in collections:
            if collection['name'] == collectionName:
                collectionId = collection['collection_id']
                break
        return collectionId

    # 人脸识别, 文件不能超过2M
    def detectFace(self, image):
        with open(image, 'rb') as image_file:
            response = self.visaulRecognition.detect_faces(images_file=image_file)
            return response

    # 分类识别
    def classify(self, image):
        with open(image, 'rb') as image_file:
            response = self.visaulRecognition.classify(images_file=image_file, threshold=0.1,
                                                       classifier_ids=self.classifier_ids)
            return response

    # 识别图片的中的文字
    def recognizeText(self, image):
        with open(image, 'rb') as image_file:
            response = self.visaulRecognition.recognize_text(images_file=image_file)
            return response
