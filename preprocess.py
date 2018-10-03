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
##INSERT FILE READING HERE
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
dataset = loadDataset("C:\\Users\\kendrick\\Desktop\\sample.csv")
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

printDataset(dataset)
#dataset looks like [ [ [word,POStag]*], emotion]
#3D array na ito

#I think ang gusto kong gawin is gawin munang words ang mga
# tags para madali tanggalin for stopword removal and POSfiltering



#/MAIN