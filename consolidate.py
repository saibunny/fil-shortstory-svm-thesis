import csv

def loadDataset(filename):
    with open(filename) as csvfile:
        lines = csv.reader(csvfile)
        return list(lines)

counti = 0
for i in range(6):
    consolidated = []
    counti = i + 1

    for j in range(4):
        countj = j+1
        # inputdirectory = "data\\validset_batch" + str(countj) + "_processed_wordcount" + str(counti)
        # inputdirectory = "data\\testsetpred_batch" + str(countj) + "_processed_wordcount" + str(counti)
        inputdirectory = "data\\validset_withnegation_batch" + str(countj) + "_processed_wordcount" + str(counti)

        dataset = loadDataset(inputdirectory + ".csv")

        for row in dataset:
            consolidated.append(row)

        # outputdirectory = "data\\consolidated_validset_processed_wordcount" + str(counti) + ".csv"
        outputdirectory = "data\\consolidated_validset_withnegation_processed_wordcount" + str(counti) + ".csv"
        with open(outputdirectory, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(consolidated)
