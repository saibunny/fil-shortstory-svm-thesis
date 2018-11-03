from spacy.lang.en import English

nlp = English()

samplesent = ["couldn't", "eating", "killed", "loving", "parties"]

for word in samplesent:
    doc = nlp(word)
    word = doc[0].lemma_
    print(word)
