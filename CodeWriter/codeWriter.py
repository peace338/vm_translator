from common.commandType import CommandType
from common.const import *

class CodeWriter:
    def __init__(self, outputFile:str):
        self.__fileHandle = open(outputFile, "w", encoding="utf-8")
        self.__count = 0
        self.__callCount = 0
        self.__staticAddr = 16
        self.__staticMap = {}

        # For FibonacciElement, StaticsTest
        self.__writeBootstrapCode()

    def __del__(self):
        self.close()

    def writeArithmetic(self, command:str):
        self.__writeln("//{}".format(command))
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
        self.__writeln("")

    def writeGoto(self, label:str):
        self.__writeln("//goto {}".format(label))
        self.__writeln("@{}".format(label))
        self.__writeln("0;JMP")
    
    def writeIf(self, label:str):
        self.__writeln("//if-goto {}".format(label))
        self.__writeln("@SP")
        self.__writeln("A=M-1")
        self.__writeln("D=M")
        self.__writeln("@SP")
        self.__writeln("M=M-1")
        self.__writeln("@{}".format(label))
        self.__writeln("D;JGT")

        self.__writeln("")

    def writeFunction(self, functionName:str, nVars:int):
        self.__writeln("//function {} {}".format(functionName, nVars))
        self.__writeln("({})".format(functionName))
        # push 0
        self.__writeln("@SP")
        self.__writeln("A=M")
        self.__writeln("M=0")
        self.__writeln("@SP")
        self.__writeln("M=M+1")
        # SP-(LCL+nVars)>=0
        self.__writeln("@SP")
        self.__writeln("D=A")
        self.__writeln("@LCL")
        self.__writeln("D=D-A")
        self.__writeln("@{}".format(nVars))
        self.__writeln("D=D-A")
        self.__writeln("@{}".format(functionName))
        self.__writeln("D;JGE")
        self.__writeln("")

    def writeCall(self, functionName:str, nVars:int):
        self.__writeln("//call {} {}".format(functionName, nVars))
        # push returnAddress
        self.__writeln("//call {} {} - push returnAddress".format(functionName, nVars))
        self.__writeln("@SP")
        self.__writeln("D=M")
        self.__push("D")
        # push LCL
        self.__writeln("//call {} {} - push LCL".format(functionName, nVars))
        self.__writeln("@LCL")
        self.__writeln("D=M")
        self.__push("D")
        # push ARG
        self.__writeln("//call {} {} - push ARG".format(functionName, nVars))
        self.__writeln("@ARG")
        self.__writeln("D=M")
        self.__push("D")
        # push THIS
        self.__writeln("//call {} {} - push THIS".format(functionName, nVars))
        self.__writeln("@THIS")
        self.__writeln("D=M")
        self.__push("D")
        # push THAT
        self.__writeln("//call {} {} - push THAT".format(functionName, nVars))
        self.__writeln("@THAT")
        self.__writeln("D=M")
        self.__push("D")
        # ARG = SP-5-nArgs
        self.__writeln("//call {} {} - ARG = SP-5-nArgs".format(functionName, nVars))
        self.__writeln("@5")
        self.__writeln("D=A")
        self.__writeln("@{}".format(nVars))
        self.__writeln("D=D+A")
        self.__writeln("@SP")
        self.__writeln("D=M-D")
        self.__writeln("@ARG")
        self.__writeln("M=D")
        
        # goto f
        self.__writeln("//call {} {} - goto f".format(functionName, nVars))
        self.__writeln("@{}".format(functionName))
        self.__writeln("0;JMP")

        #(returnAddress)
        self.__writeln("//call {} {} - (returnAddress)".format(functionName, nVars))
        self.__writeln(self.__getReturnLabel(functionName))


        self.__writeln("")

    def writeReturn(self):
        self.__writeln("//return")
        # frame = LCL
        self.__writeln("@LCL")
        self.__writeln("D=M")
        self.__writeln("@frame")
        self.__writeln("M=D")
        # retAddr = *(frame-5)
        self.__writeln("@5")
        self.__writeln("D=A")
        self.__writeln("@frame")
        self.__writeln("A=M-D")
        self.__writeln("D=M")
        self.__writeln("@retAddr")
        self.__writeln("M=D")
        # *ARG = pop()
        self.__writeln("@SP")
        self.__writeln("A=M-1")
        self.__writeln("D=M")
        self.__writeln("@ARG")
        self.__writeln("A=M")
        self.__writeln("M=D")
        # SP = ARG+1
        self.__writeln("@ARG")
        self.__writeln("D=M")
        self.__writeln("@SP")
        self.__writeln("M=D+1")
        # THAT = *(frmae-1)
        self.__writeln("@1")
        self.__writeln("D=A")
        self.__writeln("@frame")
        self.__writeln("A=M-D")
        self.__writeln("D=M")
        self.__writeln("@THAT")
        self.__writeln("M=D")
        # THIS = *(frmae-2)
        self.__writeln("@2")
        self.__writeln("D=A")
        self.__writeln("@frame")
        self.__writeln("A=M-D")
        self.__writeln("D=M")
        self.__writeln("@THIS")
        self.__writeln("M=D")
        # ARG = *(frmae-3)
        self.__writeln("@3")
        self.__writeln("D=A")
        self.__writeln("@frame")
        self.__writeln("A=M-D")
        self.__writeln("D=M")
        self.__writeln("@ARG")
        self.__writeln("M=D")
        # LCL = *(frmae-4)
        self.__writeln("@4")
        self.__writeln("D=A")
        self.__writeln("@frame")
        self.__writeln("A=M-D")
        self.__writeln("D=M")
        self.__writeln("@LCL")
        self.__writeln("M=D")
        # goto retAddr
        self.__writeln("@retAddr")
        self.__writeln("A=M")
        self.__writeln("0;JMP")
        self.__writeln("")

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
        if source not in ["D", "A"]:
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

    def __getReturnLabel(self, functionName:str) -> str:
        ret = "({}$ret.{})".format(functionName, self.__callCount)
        self.__callCount += 1

        return ret
    def __writeBootstrapCode(self):
        self.__writeln("//bootstrap")
        # SP=256
        self.__writeln("@256")
        self.__writeln("D=A")
        self.__writeln("@SP")
        self.__writeln("M=D")
        # call Sys.init
        self.writeCall("Sys.init",0)