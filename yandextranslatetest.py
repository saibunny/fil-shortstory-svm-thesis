import json, urllib.request

# key = "trnsl.1.1.20180821T035101Z.7622bc974ead6403.f3016199d1f56c33e68de316b816750e09daae43"
#
#
# def toUrlSafe(sentence):
#     return sentence.replace(" ", "+")
#
# def translateSentence(sentence):
#     sentence = toUrlSafe(sentence)
#     with urllib.request.urlopen("https://translate.yandex.net/api/v1.5/tr.json/translate"
#                                 "?key=" + key +
#                                 "&text=" + sentence +
#                                 "&lang=tl-en") as url:
#         data = json.loads(url.read().decode())
#         print(data)
#         #print(data["text"])
#         translated = "".join(data['text'])
#         return translated
#
# text = "Sinabi ko sa iyo na hindi ako kumakain ng cake"
# print(translateSentence(text))
# #Output is: I told you I'm not eating cake

class Translator:
    def __init__(self):
        self.key = "trnsl.1.1.20180821T035101Z.7622bc974ead6403.f3016199d1f56c33e68de316b816750e09daae43"

    def translateWord(self, word):
        with urllib.request.urlopen("https://translate.yandex.net/api/v1.5/tr.json/translate"
                                    "?key=" + self.key +
                                    "&text=" + word +
                                    "&lang=tl-en") as url:
            data = json.loads(url.read().decode())
            translated = "".join(data['text'])
            return translated.lower()
