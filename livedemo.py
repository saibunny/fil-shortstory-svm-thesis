import re
from taggerPy4j import POSTagger
from translator import Translator
from senticvaluer import SenticValuer
from spacy.lang.en import English
from sklearn.externals import joblib
import numpy as np 
import pandas as pd

# pangmatagalan akong nag-shopping para sa pag-ibig kasi walang katapusan


def checkNeg(row):
    for i in range(len(row)):
        if i != 0:
            prev = i-1
            if "hindi" in row[prev][0].lower() or "wala" in row[prev][0].lower():
                row[i].append("NEG")
    return row

def loadTagset(filename):
    tagset = open(filename, 'r').read().split('\n')
    return tagset

def findAffective(phrase):
    nlp = English()
    sentic = SenticValuer()

    affectiveP = []
    affective = ''
    highpolarity = 0.0
    words = phrase[0].split(" ")
    for i in range(len(words)):
        onlychars = re.sub(r'\W+', '', words[i])
        if not onlychars.isalpha():
            return ""
        doc = nlp(onlychars)
        words[i] = doc[0].lemma_
        senticVal = sentic.getSentics(words[i])
        if abs(senticVal[4]) >= highpolarity:
            affective = words[i]
            highpolarity = senticVal[4]
    affectiveP.append(affective)
    if len(phrase) == 2:
        affectiveP.append(phrase[1])
    return affectiveP

def negate(senticvals):
    for i in range(len(senticvals)):
        senticvals[i] = senticvals[i] * -1
    return senticvals

def averageSenticValues(row):
    sum = [0.0, 0.0, 0.0, 0.0, 0.0]
    for senticValues in row:
        sum[0] = sum[0] + senticValues[0]
        sum[1] = sum[1] + senticValues[1]
        sum[2] = sum[2] + senticValues[2]
        sum[3] = sum[3] + senticValues[3]
        sum[4] = sum[4] + senticValues[4]
    for i in range(len(sum)):
        sum[i] = sum[i]/len(row)

    return sum

def polarityAbs(senticval):
    return abs(senticval[4])

def retainN(row, n):
    sortedRow = sorted(row, key=polarityAbs, reverse=True)

    return sortedRow[:n]




#Accept input from user
inputsentence = input("Enter a sentence in Filipino: ")

#replace aphostrophe stuff
inputsentence = inputsentence.replace("nguni't", "ngunit")
inputsentence = inputsentence.replace("subali't", "subalit")
inputsentence = inputsentence.replace("pagka't", "pagkat")
inputsentence = inputsentence.replace("datapuwa't", "datapuwat")
inputsentence = inputsentence.replace("kahi't", "kahit")
inputsentence = inputsentence.replace("bagama't", "bagamat")
inputsentence = inputsentence.replace("isa't", "isat")
inputsentence = inputsentence.replace("'to", "ito")
inputsentence = inputsentence.replace("n'ya", "niya")
inputsentence = inputsentence.replace("s'ya", "siya")
inputsentence = inputsentence.replace("sa'yo", "sa iyo")
inputsentence = inputsentence.replace("sa'kin", "sa akin")
inputsentence = inputsentence.replace("sa'tin", "sa atin")
inputsentence = inputsentence.replace("sa'min", "sa amin")
inputsentence = inputsentence.replace("'t", " at")
inputsentence = inputsentence.replace("'y", " ay")
#remove special characters except -
inputsentence = re.sub('[^ a-zA-Z0-9\-]', '', inputsentence)

print(inputsentence)

#Tag POS
tagger = POSTagger()
inputsentence = tagger.tagSentence(inputsentence)

# print(inputsentence)

#split sentence per word
inputwords = inputsentence.split(" ")

# print(inputwords)

#split word|tag into ["word", "tag"]
for i in range(len(inputwords)):
    inputwords[i] = inputwords[i].split("|")

# print(inputwords)

#check for negation
inputwords = checkNeg(inputwords)

# print(inputwords)

#remove stop words
stopwordset = loadTagset("data\\stopwords.csv")

temp = []
for wordtag in inputwords:
    if wordtag[0] in stopwordset:
        temp.append(wordtag)
inputwords = [word for word in inputwords if word not in temp]

# print(inputwords)

#foreclipping
tagset = loadTagset("data\\tagstop5.csv")
for i in range(len(inputwords)):
    if "-" in inputwords[i][0] and inputwords[i][1] is not "FW":
        tempword = inputwords[i][0].split("-")

        while "" in tempword:
            tempword.remove("")

        temptag = []
        for j in range(len(tempword)):
            if tempword[j] is not '':
                temptag.append(tagger.returnTag(tempword[j]))
                if temptag[j] not in tagset:
                    tempwordtag = []
                    tempwordtag.append(tempword[j])
                    tempwordtag.append(temptag[j])
                    inputwords[i] = tempwordtag

# print(inputwords)

#filter POS
temp = []
for wordtag in inputwords:
    if wordtag[1] in tagset:
        temp.append(wordtag)
inputwords = [word for word in inputwords if word not in temp]

# print(inputwords)

#remove POStag
for i in range(len(inputwords)):
    inputwords[i].pop(1)

# print(inputwords)

#translate words
translator = Translator()

for i in range(len(inputwords)):
    inputwords[i][0] = translator.translateWord(inputwords[i][0])

# print(inputwords)

#lemmatize words
nlp = English()
if inputwords:
    for i in range(len(inputwords)):
        if " " in inputwords[i][0]:
            inputwords[i] = findAffective(inputwords[i])
        else:
            doc = nlp(inputwords[i][0])
            inputwords[i][0] = doc[0].lemma_

# print(inputwords)

#sentic valuing
sentic = SenticValuer()

if inputwords:
    for i in range(len(inputwords)):
        inputwords[i][0] = sentic.getSentics(inputwords[i][0])
        if len(inputwords[i]) == 2:
            inputwords[i][0] = negate(inputwords[i][0])
else:
    inputwords = [[[0.0, 0.0, 0.0, 0.0, 0.0]]]

# print(inputwords)

#retain sentic values and polarity
for i in range(len(inputwords)):
    inputwords[i] = inputwords[i][0]

# print(inputwords)

#remove blanks
while [0.0, 0.0, 0.0, 0.0, 0.0] in inputwords:
    inputwords.remove([0.0, 0.0, 0.0, 0.0, 0.0])

# print(inputwords)

#if all are 0 then the remaining sentence will be empty, hence re fill with one set of 0's
if not inputwords:
    inputwords = [[0.0, 0.0, 0.0, 0.0, 0.0]]

#retain n number of words
n = 3
inputwords = retainN(inputwords, n)

# print(inputwords)

#averaging
inputwords = averageSenticValues(inputwords)

# print(inputwords)

################# SVM PREDICTION #################

def generate_prediction(input):
    # loads the svm model
    modelfilename = "final_model_70.pkl"
    model = joblib.load(modelfilename)
    prediction = model.predict(input)
    return prediction

# appends inputwords inside another list
inputwords_2 = []
inputwords_2.append(inputwords)

# inputwords_2 = [[0.792, 0.8275, 0.00, 0.8085, 0.809], [0.855, 0.891, 0.00, 0.4885, 0.8995], [-0.33, -0.03, -0.26, -0.14, -0.17], [0.038, 0.009500000000000001, 0.0135, 0.059, 0.065]]

emotion = generate_prediction(inputwords_2)

if emotion[0] == 0:
    prediction_text = 'Neutral'
elif emotion[0] == -1:
    prediction_text = 'Negative'
else: 
    prediction_text = 'Positive'

print("Emotion: " + prediction_text)