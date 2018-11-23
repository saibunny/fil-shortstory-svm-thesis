from py4j.java_gateway import JavaGateway
class POSTagger:
    def __init__(self):
        self.gateway = JavaGateway()
        self.tagger = self.gateway.entry_point.getPost()

    def tagSentence(self, sentence):
        return self.tagger.tagPOS(sentence.lower())

    def returnTag(self, word):
        word = self.tagger.tagPOS(word)
        wordtag = word.split("|")
        return wordtag[1]
