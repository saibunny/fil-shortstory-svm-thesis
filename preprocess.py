import csv
from taggerPy4j import POSTagger
from translator import Translator
from senticvaluer import SenticValuer
from spacy.lang.en import English
import re

##FUNCTION DEFINITIONS
def loadDataset(filename):
    with open(filename) as csvfile:
        lines = csv.reader(csvfile)
        return list(lines)

def printDataset(dataset):
    print(*dataset, sep='\n')
    # for row in dataset:
    #     print(row)

def printDataset0(dataset):
    for row in dataset:
        print(row[0])

def loadTagset(filename):
    tagset = open(filename, 'r').read().split('\n')
    return tagset

def checkNeg(row):
    for i in range(len(row[0])):
        if i != 0:
            prev = i-1
            if "hindi" in row[0][prev][0].lower() or "wala" in row[0][prev][0].lower():
                row[0][i].append("NEG")
    return row

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
    for senticValues in row[0]:
        sum[0] = sum[0] + senticValues[0]
        sum[1] = sum[1] + senticValues[1]
        sum[2] = sum[2] + senticValues[2]
        sum[3] = sum[3] + senticValues[3]
        sum[4] = sum[4] + senticValues[4]
    for i in range(len(sum)):
        sum[i] = sum[i]/len(row[0])

    aveRow = []
    aveRow.append(sum)
    aveRow.append(row[1])
    return aveRow

def polarityAbs(senticval):
    return abs(senticval[4])

def onetosix(dataset):
    sixSets = []

    for i in range(6):
        count = i+1
        tempDataset = []
        for j in range(len(dataset)):
            tempRow = []
            sortedRow0 = sorted(dataset[j][0], key=polarityAbs, reverse=True)

            tempRow.append(sortedRow0[:count])
            tempRow.append(dataset[j][1])
            tempDataset.append(tempRow)
        sixSets.append(tempDataset)

    return sixSets
##/FUNCTION DEFINITIONS


#MAIN
filename = "validset_withnegation"

inputdirectory = "data\\" + filename

print(inputdirectory)
dataset = loadDataset(inputdirectory + ".csv")
print("dataset loaded")

print("start replace apostrophe stuff")
for i in range(len(dataset)):
    dataset[i][0] = dataset[i][0].replace("nguni’t", "ngunit")
    dataset[i][0] = dataset[i][0].replace("subali’t", "subalit")
    dataset[i][0] = dataset[i][0].replace("pagka’t", "pagkat")
    dataset[i][0] = dataset[i][0].replace("datapuwa’t", "datapuwat")
    dataset[i][0] = dataset[i][0].replace("kahi’t", "kahit")
    dataset[i][0] = dataset[i][0].replace("bagama’t", "bagamat")
    dataset[i][0] = dataset[i][0].replace("isa't", "isat")
    dataset[i][0] = dataset[i][0].replace("’to", "ito")
    dataset[i][0] = dataset[i][0].replace("n’ya", "niya")
    dataset[i][0] = dataset[i][0].replace("s’ya", "siya")
    dataset[i][0] = dataset[i][0].replace("sa’yo", "sa iyo")
    dataset[i][0] = dataset[i][0].replace("sa’kin", "sa akin")
    dataset[i][0] = dataset[i][0].replace("sa’tin", "sa atin")
    dataset[i][0] = dataset[i][0].replace("sa’min", "sa amin")
    dataset[i][0] = dataset[i][0].replace("’t", " at")
    dataset[i][0] = dataset[i][0].replace("’y", " ay")
print("end replace apostrophe stuff")

printDataset(dataset)

print("start remove special chars")
for i in range(len(dataset)):
    dataset[i][0] = re.sub('[^ a-zA-Z0-9\-]', '', dataset[i][0])
print("end remove special chars")

printDataset(dataset)

tagger = POSTagger()

print("start tagging")
for row in dataset:
    row[0] = tagger.tagSentence(row[0])[:-1]
    # row[0] = row[0][:-1]
print("end tagging")

print("start splitting by space")
for row in dataset:
    row[0] = row[0].split(" ")
print("end splitting by space")

print("start splitting words and tags")
for row in dataset:
    for i in range(len(row[0])):
        row[0][i] = row[0][i].split("|")
print("end splitting words and tags")

print("start finding negation")
for i in range(len(dataset)):
    dataset[i] = checkNeg(dataset[i])
print("end finding negation")

print("start stopword removal")
stopwordset = loadTagset("data\\stopwords.csv")

for row in dataset:
    temp = []
    for wordtag in row[0]:
        if wordtag[0] in stopwordset:
            temp.append(wordtag)
    row[0] = [word for word in row[0] if word not in temp]
print("end stopword removal")

print("start foreclipping")
tagset = loadTagset("data\\tagstop5.csv")
for row in dataset:
    for i in range(len(row[0])):
        if "-" in row[0][i][0] and row[0][i][1] is not "FW":
            tempword = row[0][i][0].split("-")

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
                        row[0][i] = tempwordtag
print("end foreclipping")

print("start filtering POS")

for row in dataset:
    temp = []
    for wordtag in row[0]:
        if wordtag[1] in tagset:
            temp.append(wordtag)
    row[0] = [word for word in row[0] if word not in temp]
print("end filtering POS")

print("start removing POStag")
for row in dataset:
    for i in range(len(row[0])):
        row[0][i].pop(1)
print("end removing POStag")

print("Start translation")
translator = Translator()

translations = []

count = 0
for row in dataset:
    untransrow = "<"
    transrow = ">"

    temptransrow = []

    for i in range(len(row[0])):
        untransrow = untransrow + "|" + row[0][i][0]
        temmie = translator.translateWord(row[0][i][0])
        transrow = transrow + "|" + temmie
        row[0][i][0] = temmie

    temptransrow.append(untransrow)
    temptransrow.append(transrow)

    translations.append(temptransrow)

    count = count + 1
    print(str(count) + " " + untransrow + "|||||" + transrow)
print("End translation")

print("Start lemmatization")
nlp = English()
for row in dataset:
    if row[0]:
        for i in range(len(row[0])):
            if " " in row[0][i][0]:
                row[0][i][0] = findAffective(row[0][i])
            else:
                doc = nlp(row[0][i][0])
                row[0][i][0] = doc[0].lemma_
print("end lemmatization")

print("start sentic valuing")
sentic = SenticValuer()

for row in dataset:
    if row[0]:
        for i in range(len(row[0])):
            row[0][i][0] = sentic.getSentics(row[0][i][0])
            if len(row[0][i]) == 2:
                row[0][i][0] = negate(row[0][i][0])
    else:
            row[0] = [[[0.0, 0.0, 0.0, 0.0, 0.0]]]
print("end sentic valuing")

print("start retaining sentic values and polarity")
for row in dataset:
    for i in range(len(row[0])):
        row[0][i] = row[0][i][0]
print("end retaining sentic values and polarity")

print("start removing blanks")
for i in range(len(dataset)):
    while [0.0, 0.0, 0.0, 0.0, 0.0] in dataset[i][0]:
        dataset[i][0].remove([0.0, 0.0, 0.0, 0.0, 0.0])

print("end removing blanks")

print("start refill with 0")
for i in range(len(dataset)):
    if not dataset[i][0]:
        dataset[i][0] = [[0.0, 0.0, 0.0, 0.0, 0.0]]

print("end refill with 0")

print("start averaging")

sixSets = onetosix(dataset)
for i in range(len(sixSets)):
    for j in range(len(sixSets[i])):
        sixSets[i][j] = averageSenticValues(sixSets[i][j])
print("end averaging")

print("start writing to file")

for i in range(len(sixSets)):
    count = i+1
    directory = inputdirectory + "_processed_wordcount" + str(count) + '.csv'

    finalDataset = []

    for j in range(len(sixSets[i])):
        newRow = []
        newRow.append(sixSets[i][j][0][0])
        newRow.append(sixSets[i][j][0][1])
        newRow.append(sixSets[i][j][0][2])
        newRow.append(sixSets[i][j][0][3])
        newRow.append(sixSets[i][j][0][4])
        newRow.append(sixSets[i][j][1])
        newRow.append(translations[j][0])
        newRow.append(translations[j][1])
        finalDataset.append(newRow)

    with open(directory, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(finalDataset)

print("end writing to file")

#/MAIN