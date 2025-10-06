class Parser:
    def __init__(self, inputFile:str):
        self.fileHandle = open(inputFile, "r", encoding="utf-8")

