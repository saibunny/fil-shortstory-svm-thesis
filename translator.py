import json, urllib.request

class Translator:
    def __init__(self):
        self.key = ""

    def translateWord(self, word):
        for i in range(10):
            try:
                with urllib.request.urlopen("https://translate.yandex.net/api/v1.5/tr.json/translate"
                                            "?key=" + self.key +
                                            "&text=" + word +
                                            "&lang=tl-en") as url:
                    data = json.loads(url.read().decode())
                    translated = "".join(data['text'])
                    return translated.lower()
            except Exception as e:
                print("Try number " + str(i) + " for word :" + word)