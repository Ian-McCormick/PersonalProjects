import json
import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Tag:
    def __init__(self, symbol, type, name) :
        self.symbol = symbol
        self.type = type
        self.name = name

def main():
    inputTXT = open(CURRENT_DIRECTORY + "\\tags.txt", "r")
    outputJSON = open(CURRENT_DIRECTORY + "\\stockInfo.json", "w+")
    stockObjects = []
    for rawStock in inputTXT.readlines():
        splitData = rawStock.split(", ")
        symbol = splitData[0].strip()
        ver = splitData[1].strip()
        name = splitData[2].strip()
        stockObject = Tag(symbol, ver, name)
        stockObjects.append(stockObject)
    
    jsonString = json.dumps({"Securities": [tag.__dict__ for tag in stockObjects]}, indent=4)
    outputJSON.write(jsonString)
    inputTXT.close()
    outputJSON.close()

main()