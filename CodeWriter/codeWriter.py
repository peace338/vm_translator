from common.commandType import CommandType

class CodeWriter:
    def __init__(self, outputFile:str):
        self.fileHandle = open(outputFile, "w", encoding="utf-8")
    
    def writeArithmetic(self, command:str):
        pass

    def writePushPop(self, command:CommandType, segment:str, index:int):
        pass

    def close(self):
        self.fileHandle.close()
