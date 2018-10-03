from py4j.java_gateway import JavaGateway
gateway = JavaGateway()

tagger = gateway.entry_point.getPost()


sentence = "Ang mabilis na soro ay tinalunan ang asong tamad. Mahal ko ang aking isda."
print(tagger.tagPOS(sentence))





class POSTagger:
    def __init__(self):
        self.gateway = JavaGateway()
        self.tagger = self.gateway.entry_point.getPost()

    def tagSentence(self, sentence):
        return self.tagger.tagPOS(sentence)
