import re
from py4jTest import POSTagger
from yandextranslatetest import Translator
from senticnettest import SenticValuer
from spacy.lang.en import English

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

#remove special characters except -
inputsentence = re.sub('[^ a-zA-Z0-9\-]', '', inputsentence)

#Tag POS
tagger = POSTagger()
inputsentence = tagger.tagSentence(inputsentence)

#split sentence per word
inputwords = inputsentence.split(" ")

#split word|tag into ["word", "tag"]
for i in range(len(inputwords)):
    inputwords[i] = inputwords[i].split("|")

#check for negation
inputwords = checkNeg(inputwords)

print(inputwords)

#remove stop words
stopwordset = loadTagset("data\\stopwords.csv")

temp = []
for wordtag in inputwords:
    if wordtag[0] in stopwordset:
        temp.append(wordtag)
inputwords = [word for word in inputwords if word not in temp]


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

print(inputwords)

#filter POS
temp = []
for wordtag in inputwords:
    if wordtag in tagset:
        temp.append(wordtag)
inputwords = [word for word in inputwords if word not in temp]
print(inputwords)

#remove POStag
for i in range(len(inputwords)):
    inputwords[i].pop(1)

print(inputwords)

#translate words
translator = Translator()

for i in range(len(inputwords)):
    inputwords[i][0] = translator.translateWord(inputwords[i][0])

print(inputwords)

#lemmatize words
nlp = English()
if inputwords:
    for i in range(len(inputwords)):
        if " " in inputwords[i][0]:
            inputwords[i] = findAffective(inputwords[i])
        else:
            doc = nlp(inputwords[i][0])
            inputwords[i][0] = doc[0].lemma_

print(inputwords)

#sentic valuing
sentic = SenticValuer()

if inputwords:
    for i in range(len(inputwords)):
        inputwords[i][0] = sentic.getSentics(inputwords[i][0])
        if len(inputwords[i]) == 2:
            inputwords[i][0] = negate(inputwords[i][0])
else:
    inputwords = [[[0.0, 0.0, 0.0, 0.0, 0.0]]]

print(inputwords)

#retain sentic values and polarity
for i in range(len(inputwords)):
    inputwords[i] = inputwords[i][0]

print(inputwords)

#remove blanks
while [0.0, 0.0, 0.0, 0.0, 0.0] in inputwords:
    inputwords.remove([0.0, 0.0, 0.0, 0.0, 0.0])

print(inputwords)

#retain n number of words
n = 3
inputwords = retainN(inputwords, n)

print(inputwords)

#averaging
inputwords = averageSenticValues(inputwords)

print(inputwords)