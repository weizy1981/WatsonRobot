from os import remove
from watson_developer_cloud import TextToSpeechV1
from watson_developer_cloud import SpeechToTextV1

class WatsonText2Speech():
    bluemix_username_text2speech = '83469b85-efcd-4baa-804a-3bd4043a2c1e'
    bluemix_password_text2speech = 'Ix8H8TqDTt0u'
    bluemix_watsonvoice_en_text2speech = 'en-US_AllisonVoice'
    text_to_speech = None

    def __init__(self):
        self.text_to_speech = TextToSpeechV1(
            username=self.bluemix_username_text2speech,
            password=self.bluemix_password_text2speech,
            x_watson_learning_opt_out=True)  # Optional flag

    def text2speech(self, fileName='', message=''):
        if fileName == '':
            fileName = '/Users/wzy/Documents/workspace/FirstFlask/tmp/output.wav'
        #print(fileName)

        if message == '':
            message = 'Hello world!'

        try:
            remove(fileName)
        except:
            print('there is no file exist')

        with open(fileName, 'wb') as audio_file:
            audio_file.write(
                self.text_to_speech.synthesize(message, accept='audio/wav', voice=self.bluemix_watsonvoice_en_text2speech))


class WatsonSpeech2Text:

    bluemix_username_speech2text = '2a395ca9-9d31-4524-ab35-a17d5908b1ec'
    bluemix_password_speech2text = 'BBHk2G1yMszb'
    bluemix_language_model_en_speech2text = 'en-US_BroadbandModel'
    speech_to_text = None

    def __init__(self):
        self.speech_to_text = SpeechToTextV1(
            username=self.bluemix_username_speech2text,
            password=self.bluemix_password_speech2text,
            x_watson_learning_opt_out=False)


    def speech2text(self, fileName=''):
        if fileName == '':
            fileName = '/Users/wzy/Documents/workspace/FirstFlask/tmp/input.wav'

        res = []

        with open(fileName, 'rb') as audio_file:
            text_dic = self.speech_to_text.recognize(audio_file, content_type='audio/wav',
                                                model=self.bluemix_language_model_en_speech2text,
                                                inactivity_timeout=-1,
                                                continuous=True,
                                                timestamps=False,
                                                word_confidence=False)
            # print(text_dic)
            text_list = text_dic['results']

            for msgDic in text_list:
                msgList = msgDic['alternatives']
                msgDic = msgList[0]
                message_txt = msgDic['transcript']
                confidence_rate = msgDic['confidence']
                res.append(message_txt)
                #print(confidence_rate)
                #print(message_txt)

        return res
