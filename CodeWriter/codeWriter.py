from common.commandType import CommandType
from common.const import Bool

class CodeWriter:
    def __init__(self, outputFile:str):
        self.__fileHandle = open(outputFile, "w", encoding="utf-8")
        self.__count = 0
    
    def __del__(self):
        self.close()

    def writeArithmetic(self, command:str):
        self.__writeln("//"+command)
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
            
            self.__writeln("")

        elif command == "eq":
            self.__comparison("JEQ", self.__count)
            self.__writeln("")
            self.__count += 1
        elif command == "lt":
            self.__comparison("JLT", self.__count)
            self.__writeln("")
            self.__count += 1
        elif command == "gt":
            self.__comparison("JGT", self.__count)
            self.__writeln("")
            self.__count += 1
        
        elif command == "not":
            self.__pop("D")
            
            #push
            self.__writeln("M=!D")
            self.__stackPointerAddOne()
            
            self.__writeln("")
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
        elif segment == "pointer":
            pass
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
            self.__stackPointerSubOne()

            #*addr=*SP
            self.__writeln("@SP")
            self.__writeln("D=M")
            self.__writeln("@addr")
            self.__writeln("M=D")
            
        elif command == CommandType.C_PUSH:
            #*SP=*addr
            self.__writeln("@addr")
            self.__writeln("A=M")
            self.__writeln("D=A")
            self.__writeln("@SP")
            self.__writeln("A=M")
            self.__writeln("M=D")

            # SP++
            self.__stackPointerAddOne()

        else:
            raise AssertionError("Unknown command")
        
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
            self.__writeln("@SP")
            self.__writeln("A=M")
            self.__writeln("M=D")
            # SP++
            self.__stackPointerAddOne()

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
    def __processing(self, operator:str):
        if operator not in ["+", "-", "&", "|"]:
            raise AssertionError(f"Unkown operator:{operator} for processing")
        self.__pop("D")
        self.__pop("M")
        
        # push
        self.__writeln(f"M=M{operator}D")
        self.__stackPointerAddOne()