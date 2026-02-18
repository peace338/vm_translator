from common.commandType import CommandType
from common.const import *

class CodeWriter:
    def __init__(self, outputFile:str):
        self.__fileHandle = open(outputFile, "w", encoding="utf-8")
        self.__count = 0
        self.__staticAddr = 16
        self.__staticMap = {}

    def __del__(self):
        self.close()

    def writeArithmetic(self, command:str):
        
        if command == "add":
            self.__processing("+")
            self.__writeln("")
        elif command == "sub":
            self.__processing("-")
            self.__writeln("")
        elif command == "and":
            self.__processing("&")
        elif command == "or":
            self.__processing("|")
        elif command == "neg":
            self.__pop("D")
            #push
            self.__writeln("M=-D")
            self.__stackPointerAddOne()
        elif command == "not":
            self.__pop("D")
            #push
            self.__writeln("M=!D")
            self.__stackPointerAddOne()
        elif command == "eq":
            self.__comparison("JEQ", self.__count)
            self.__count += 1
        elif command == "lt":
            self.__comparison("JLT", self.__count)
            self.__count += 1
        elif command == "gt":
            self.__comparison("JGT", self.__count)
            self.__count += 1
        else:
            raise AssertionError(f"Unknown command: {command}")

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
            self.__pushConstant(index)
        elif segment == "local":
            self.__calcAddr("LCL", index)
            self.__processPushPop(command)
        elif segment == "argument":
            self.__calcAddr("ARG", index)
            self.__processPushPop(command)
        elif segment == "this":
            self.__calcAddr("THIS", index)
            self.__processPushPop(command)
        elif segment == "that":
            self.__calcAddr("THAT", index)
            self.__processPushPop(command)
        elif segment == "temp":
            self.__calcAddrForTempSegment(f"{BaseAddr.TEMP}", index)
            self.__processPushPop(command)
        elif segment == "pointer":
            if index == "0":
                baseAddr = BaseAddr.THIS
            elif index == "1":
                baseAddr = BaseAddr.THAT
            else:
                raise ArithmeticError(f"Unexpected index:{index} for pointer segement")
            self.__processPushPopForSpecificAddr(baseAddr, command)
        elif segment == "static":
            if command == CommandType.C_PUSH:                
                self.__processPushPopForSpecificAddr(self.__staticMap[index], command)
            elif command == CommandType.C_POP:
                self.__staticMap[index] = self.__staticAddr
                self.__processPushPopForSpecificAddr(self.__staticMap[index], command)
                self.__staticAddr += 1
                self.__staticAddrVerification()
            else:
                raise AssertionError("Unknown Command")
        else:
            raise AssertionError("Unknown segment:", segment)
        

        
        self.__writeln("")

    def setFileName(self, filename:str):
        pass

    def writeLabel(self, label:str):
        self.__writeln("//label {}".format(label))
        self.__writeln("({})".format(label))

    def writeGoto(self, label:str):
        pass
    
    def writeIf(self, label:str):
        self.__writeln("//if-goto {}".format(label))
        self.__writeln("@SP")
        self.__writeln("D=M")
        self.__writeln("@{}".format(label))
        self.__writeln("M=D;JGT")

    def writeFunction(self, functionName:str, nVars:int):
        pass

    def writeCall(self, functionName:str, nVars:int):
        pass

    def writeReturn(self):
        pass

    def close(self):
        self.__fileHandle.close()

    def __writeln(self, text:str):
        self.__fileHandle.write(text+"\n")
        
    def __stackPointerAddOne(self):
        self.__writeln("@SP")
        self.__writeln("M=M+1")

    def __stackPointerSubOne(self):
        self.__writeln("@SP")
        self.__writeln("M=M-1")

    def __pushBool(self, value:Bool):
        self.__writeln("@SP")
        self.__writeln("A=M")
        self.__writeln(f"M={value}")
        self.__stackPointerAddOne()
    
    def __pushConstant(self, value:int):
            # push constant i
            # *SP=i    
            self.__writeln("@"+value)
            self.__writeln("D=A")
            self.__push("D")

    def __comparison(self, jumpCommand:str, count:int):
        self.__pop("D")
        self.__pop("M")
        self.__writeln("D=M-D")
        
        # JEQ
        self.__writeln(f"@TRUE_{count}")
        self.__writeln(f"D;{jumpCommand}")
        
        # push FALSE
        self.__pushBool(Bool.FALSE)
        self.__writeln(f"@COMP_END_{count}")
        self.__writeln("0;JMP")
        # TRUE LABEL
        self.__writeln(f"(TRUE_{count})")
        # push TRUE
        self.__pushBool(Bool.TRUE)
        self.__writeln(f"(COMP_END_{count})")

    def __pop(self, dest:str):
        if dest not in ["D", "A", "M"]:
            raise AssertionError(f"Unkown destionation:{dest} of pop")
        # SP --
        self.__stackPointerSubOne()
        #D=*SP
        self.__writeln("@SP")
        self.__writeln("A=M")
        
        if dest != "M":
            self.__writeln(f"{dest}=M")

    def __push(self, source:str):
        if source not in ["D", "A", "M"]:
            raise AssertionError(f"Unkown destionation:{source} of pop")
        self.__writeln("@SP")
        self.__writeln("A=M")
        self.__writeln(f"M={source}")
        # SP++
        self.__stackPointerAddOne()

    def __processing(self, operator:str):
        if operator not in ["+", "-", "&", "|"]:
            raise AssertionError(f"Unkown operator:{operator} for processing")
        self.__pop("D")
        self.__pop("M")
        
        # push
        self.__writeln(f"M=M{operator}D")
        self.__stackPointerAddOne()

    def __calcAddr(self, segmentSymbol:str, index:str):
        # addr=basePointer + index
        self.__writeln(f"@{index}")
        self.__writeln("D=A")
        self.__writeln(f"@{segmentSymbol}")
        self.__writeln("D=M+D")
        self.__writeln("@addr")
        self.__writeln("M=D")
    
    def __calcAddrForTempSegment(self, segmentSymbol:str, index:str):
        # addr=basePointer + index
        self.__writeln(f"@{index}")
        self.__writeln("D=A")
        self.__writeln(f"@{segmentSymbol}")
        self.__writeln("D=A+D")
        self.__writeln("@addr")
        self.__writeln("M=D")

    def __calcAddrForPointerSegment(self, segmentSymbol:str):
        # addr=basePointer + index
        self.__writeln(f"@{segmentSymbol}")
        self.__writeln("D=A+D")
        self.__writeln("@addr")
        self.__writeln("M=D")
    
    def __processPushPop(self, command:CommandType):
        if command == CommandType.C_POP:
            # D = RAM[SP--]
            self.__pop("D") 
            # *addr=D
            self.__writeln("@addr")
            self.__writeln("A=M")
            self.__writeln("M=D")
            
        elif command == CommandType.C_PUSH:
            # D=*addr
            self.__writeln("@addr")
            self.__writeln("A=M")
            self.__writeln("D=M")
            # RAM[SP++] = D
            self.__push("D")

        else:
            raise AssertionError(f"Unknown command:{command}")
    
    def __processPushPopForSpecificAddr(self, baseAddr:int, command:CommandType):
        if command == CommandType.C_POP:
            # D = RAM[SP--]
            self.__pop("D") 
            # baseAddr=D
            self.__writeln(f"@{baseAddr}")
            self.__writeln("M=D")
            
        elif command == CommandType.C_PUSH:
            # D=baseAddr
            self.__writeln(f"@{baseAddr}")
            self.__writeln("D=M")
            # RAM[SP++] = D
            self.__push("D")

        else:
            raise AssertionError(f"Unknown command:{command}")
        
    def __staticAddrVerification(self):
        if self.__staticAddr > BaseAddr.STACK:
            raise AssertionError(f"Static address:{self.__staticAddr} should be smaller than {BaseAddr.STACK}")
