#import for csv
import csv

#import for tagger
from py4jTest import POSTagger

#import for translator
from yandextranslatetest import Translator

#import for sentic value tagger
from senticnettest import SenticValuer

#import for english lemmatizer
from spacy.lang.en import English

#import for sorting
from operator import itemgetter

import re

##ACTUAL CODE

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
    # loaded = []
    # tagset = []
    # with open(filename) as csvfile:
    #     lines = csv.reader(csvfile)
    #     loaded = list(lines)
    # for tag in loaded:
    #     tagset.append(tag[0])
    # return tagset

def findAffective(phrase):
    nlp = English()
    sentic = SenticValuer()

    affective = ''
    highpolarity = 0.0
    words = phrase.split(" ")
    print(words)
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

    return affective


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
batchnum = 37
# inputdirectory = "data\\validset_batch" + str(batchnum)
inputdirectory = "data\\sample"
dataset = loadDataset(inputdirectory + ".csv")
#dataset looks like [sentence, emotion]

print("dataset loaded")

tagger = POSTagger()

print("start tagging")
for row in dataset:
    row[0] = tagger.tagSentence(row[0])[:-1]
    # row[0] = row[0][:-1]
#row in dataset looks like [sentence with POStag, emotion]
print("end tagging")

print("start splitting by space")
for row in dataset:
    row[0] = row[0].split(" ")
#row in dataset looks like [ [word|POStag*], emotion]
#dapat + pero kleen star na lang. meaning there is more than 1 word per row
#an array within an array
print("end splitting by space")

print("start splitting words and tags")
for row in dataset:
    for i in range(len(row[0])):
        row[0][i] = row[0][i].split("|")
#dataset looks like [ [ [word,POStag]*], emotion]
#3D array na ito
print("end splitting words and tags")


print("start stopword removal")
stopwordset = loadTagset("data\\stopwords.csv")

for row in dataset:
    temp = []
    for wordtag in row[0]:
        # temp = [word for word in wordtag[1] if word in tagset]
        if wordtag[0] in stopwordset:
            temp.append(wordtag)
    row[0] = [word for word in row[0] if word not in temp]
#dataset still looks like the one from earlier except retain most affective POS
print("end stopword removal")

printDataset(dataset)

print("start foreclipping")
tagset = loadTagset("data\\tagstop5.csv")
for row in dataset:
    for i in range(len(row[0])):
        if "-" in row[0][i][0] and row[0][i][1] is not "FW":
            tempword = row[0][i][0].split("-")
            temptag = []
            for j in range(len(tempword)):
                temptag.append(tagger.returnTag(tempword[j]))
                if temptag[j] not in tagset:
                    tempwordtag = []
                    tempwordtag.append(tempword[j])
                    tempwordtag.append(temptag[j])
                    row[0][i] = tempwordtag
print("end foreclipping")

printDataset(dataset)


print("start filtering POS")

for row in dataset:
    temp = []
    for wordtag in row[0]:
        # temp = [word for word in wordtag[1] if word in tagset]
        if wordtag[1] in tagset:
            temp.append(wordtag)
    row[0] = [word for word in row[0] if word not in temp]
#dataset still looks like the one from earlier except retain most affective POS
print("end filtering POS")


print("start replacing [word|tag] list by word")

for row in dataset:
    for i in range(len(row[0])):
        row[0][i] = row[0][i][0]
# dataset = [[j.lower() for j in i] for i in dataset]

#dataset now looks like [ [word]*, emotion]
print("end replacing [word|tag] list by word")


print("Start translation")
translator = Translator()

count = 0
for row in dataset:
    untransrow = ""
    transrow = ""
    for i in range(len(row[0])):
        untransrow = untransrow + "|" + row[0][i]
        temmie = translator.translateWord(row[0][i])
        transrow = transrow + "|" + temmie
        row[0][i] = temmie
    count = count + 1
    print(str(count) + " " + untransrow + "|||||" + transrow)
print("End translation")
#dataset still looks like the one from before except translated to english

print("Start lemmatization")
#next is lemmatizer
nlp = English()
for row in dataset:
    if row[0]:
        for i in range(len(row[0])):
            if " " in row[0][i]:
                row[0][i] = findAffective(row[0][i])
            else:
                doc = nlp(row[0][i])
                row[0][i] = doc[0].lemma_

#dataset still looks like the one from before but lemmatized
print("end lemmatization")

print("start sentic valuing")
#next up is senticnet and keep in mind the blank resulting row[0] make the sentic value for that all 0's
sentic = SenticValuer()

for row in dataset:
    if row[0]:
        for i in range(len(row[0])):
            row[0][i] = sentic.getSentics(row[0][i])
    else:
            row[0] = [[0.0, 0.0, 0.0, 0.0, 0.0]]
#the dataset now looks like [ [sentic values]*, emotion]
print("end sentic valuing")


printDataset(dataset)

print("start averaging")

sixSets = onetosix(dataset)
for i in range(len(sixSets)):
    for j in range(len(sixSets[i])):
        sixSets[i][j] = averageSenticValues(sixSets[i][j])
print("end averaging")

print("start writing to file")

#Write dataset to file
for i in range(len(sixSets)):
    count = i+1
    directory = inputdirectory + "_processed_wordcount" + str(count) + '.csv'

    finalDataset = []

    for row in sixSets[i]:
        newRow = []
        newRow.append(row[0][0])
        newRow.append(row[0][1])
        newRow.append(row[0][2])
        newRow.append(row[0][3])
        newRow.append(row[0][4])
        newRow.append(row[1])
        finalDataset.append(newRow)

    with open(directory,'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(finalDataset)

print("end writing to file")

print("complete batch #" + str(batchnum))
#/MAIN