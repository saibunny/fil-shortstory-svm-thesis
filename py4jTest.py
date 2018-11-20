from py4j.java_gateway import JavaGateway
# gateway = JavaGateway()
#
# tagger = gateway.entry_point.getPost()
#
#
# sentence = "high school. taga-punch, mag-shopping, pala-iyot pala iyot taga-bake taga bake nag i strike nag-i-strike"
# print(tagger.tagPOS(sentence))



class POSTagger:
    def __init__(self):
        self.gateway = JavaGateway()
        self.tagger = self.gateway.entry_point.getPost()

    def tagSentence(self, sentence):
        return self.tagger.tagPOS(sentence)

    def returnTag(self, word):
        word = self.tagger.tagPOS(word)
        wordtag = word.split("|")
        return wordtag[1]




# tagger = POSTagger()
#
# print(tagger.returnTag("high"))
