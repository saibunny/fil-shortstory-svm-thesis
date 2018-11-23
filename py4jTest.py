from py4j.java_gateway import JavaGateway
import re

class POSTagger:
    def __init__(self):
        self.gateway = JavaGateway()
        self.tagger = self.gateway.entry_point.getPost()

    def tagSentence(self, sentence):
        return self.tagger.tagPOS(sentence.lower())

    def returnTag(self, word):
        word = self.tagger.tagPOS(word)
        wordtag = word.split("|")
        return re.sub('[^a-zA-Z0-9\-]', '', wordtag[1])