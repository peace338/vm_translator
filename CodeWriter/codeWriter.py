from common.commandType import CommandType
\
class CodeWriter:
    def __init__(self, outputFile:str):
        self.__fileHandle = open(outputFile, "w", encoding="utf-8")
    
    def __del__(self):
        self.close()

    def writeArithmetic(self, command:str):
        self.__writeln("//"+command)
        self.__writeln("")
    def writePushPop(self, command:CommandType, segment:str, index:int):
        
        if command == CommandType.C_POP:
            commandStr = "pop"
        elif command == CommandType.C_PUSH:
            commandStr = "push"
        else:
            raise AssertionError("Unknown Command")
        
        self.__writeln("//"+commandStr+" "+segment+" "+index)

        if segment == "constant":    
            # push constant i
            # *SP=i    
            self.__writeln("@"+index)
            self.__writeln("D=A")
            self.__writeln("@SP")
            self.__writeln("A=M")
            self.__writeln("M=D")
            # SP++
            self.__writeln("@SP")
            self.__writeln("M=M+1")
            self.__writeln("")
            # constant segment에서 pop은 없음.
            return 
        
        elif segment == "local":
            segmentSymbol = "LCL"
        elif segment == "argument":
            segmentSymbol = "ARG"
        elif segment == "this":
            segmentSymbol = "THIS"
        elif segment == "that":
            segmentSymbol = "THAT"
        elif segment == "temp":
            segmentSymbol = "TEMP"
        else:
            raise AssertionError("Unknown segment:", segment)

        # addr=basePointer + index
        self.__writeln("@"+index)
        self.__writeln("D=A")
        self.__writeln("@"+segmentSymbol)
        self.__writeln("D=M+D")
        self.__writeln("@addr")
        self.__writeln("M=D")

        if command == CommandType.C_POP:
            # SP--
            self.__writeln("@SP")
            self.__writeln("M=M-1")

            #*addr=*SP
            self.__writeln("@SP")
            self.__writeln("D=M")
            self.__writeln("@addr")
            self.__writeln("M=D")
            
        elif command == CommandType.C_PUSH:
            #*SP=*addr
            self.__writeln("@addr")
            self.__writeln("D=A")
            self.__writeln("@SP")
            self.__writeln("A=M")
            self.__writeln("M=D")

            # SP++
            self.__writeln("@SP")
            self.__writeln("M=M+1")

        else:
            raise AssertionError("Unknown command")
        
        self.__writeln("")


    def close(self):
        self.__fileHandle.close()

    def __writeln(self, text:str):
        self.__fileHandle.write(text+"\n")
