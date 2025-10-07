from common.commandType import CommandType

class CodeWriter:
    def __init__(self, outputFile:str):
        self.fileHandle = open(outputFile, "w", encoding="utf-8")
    
    def writeArithmetic(self, command:str):
        self.fileHandle.write("//"+command+"\n")

    def writePushPop(self, command:CommandType, segment:str, index:int):
        
        if command == CommandType.C_POP:
            commandStr = "pop"
        elif command == CommandType.C_PUSH:
            commandStr = "push"
        else:
            raise AssertionError("Unknown Command")
        
        self.fileHandle.write("//"+commandStr+" "+segment+" "+index+"\n")

    def close(self):
        self.fileHandle.close()
