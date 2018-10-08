#TODO: Insert imports for file reading and other stuff
#import for csv
import csv

#import for tagger
from py4jTest import POSTagger

#import for translator
from yandextranslatetest import Translator

#import for sentic value tagger
from senticnettest import SenticValuer


##ACTUAL CODE

##FUNCTION DEFINITIONS
def loadDataset(filename):
    with open(filename) as csvfile:
        lines = csv.reader(csvfile)
        return list(lines)

def printDataset(dataset):
    for row in dataset:
        print(row)

def printDataset0(dataset):
    for row in dataset:
        print(row[0])

def loadTagset(filename):
    loaded = []
    tagset = []
    with open(filename) as csvfile:
        lines = csv.reader(csvfile)
        loaded = list(lines)
    for tag in loaded:
        tagset.append(tag[0])
    return tagset
##/FUNCTION DEFINITIONS

##IMPORT EXAMPLES

# #POSTAGGER PART##
# tagger = POSTagger()
# sentence = "Ilang kabobohan kaya ang magagawa ni ma'am Janette sa atin sa sem?"
# print(tagger.tagSentence(sentence))
# #/POSTAGGER PART##
# #INSERT STOP WORD REMOVAL HERE
# #INSERT POS FILTERING HERE PERO KAILANGAN NG TALLY SHIT

""" COMMENT WHEN NO INTERNET, UNCOMMENT WHEN HAVE INTERNET
##TRANSLATOR PART##
word = 'bobo'
translator = Translator()
print(translator.translateWord(word))
##/TRANSLATOR PART##
"""
##INSERT LEMMATIZATION PART HERE

# ##SENTIC VALUE TAGGER PART##
# translatedword = 'stupid'
# sentic = SenticValuer()
# print(sentic.getSentics(translatedword))
# ##/SENTIC VALUE TAGGER PART##

##INSERT PART FOR THE FEATURE SELECTION PART

##/IMPORT EXAMPLES

#MAIN
dataset = loadDataset("data\\sample.csv")
#dataset looks like [sentence, emotion]

tagger = POSTagger()

for row in dataset:
    row[0] = tagger.tagSentence(row[0])
    row[0] = row[0][:-1]
#row in dataset looks like [sentence with POStag, emotion]

for row in dataset:
    row[0] = row[0].split(" ")
#row in dataset looks like [ [word|POStag*], emotion]
#dapat + pero kleen star na lang. meaning there is more than 1 word per row
#an array within an array
for row in dataset:
    for i in range(len(row[0])):
        row[0][i] = row[0][i].split("|")

#dataset looks like [ [ [word,POStag]*], emotion]
#3D array na ito

#I think ang gusto kong gawin is gawin munang words ang mga
# tags para madali tanggalin for stopword removal and POSfiltering
tagset = loadTagset("data\\tags.csv")

print(printDataset(dataset))
print('AFTER')

for row in dataset:
    temp = []
    for wordtag in row[0]:
        if wordtag[1] in tagset:
            temp.append(wordtag)
    row[0] = [word for word in row[0] if word not in temp]


print(printDataset(dataset))
#/MAIN