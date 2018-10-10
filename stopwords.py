import csv

def loadTagset(filename):
    loaded = []
    tagset = []
    with open(filename) as csvfile:
        lines = csv.reader(csvfile)
        loaded = list(lines)
    for tag in loaded:
        tagset.append(tag[0])
    return tagset



tagset = loadTagset("data\\tags.csv")
if "LM" in tagset:
    print("yes")
