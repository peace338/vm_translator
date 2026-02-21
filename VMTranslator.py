import argparse
import os
from Parser.parser import Parser
from CodeWriter.codeWriter import CodeWriter
from common.commandType import CommandType

class VMTranslator:
    def __init__(self, input:str):
        self.filelist = None
        if os.path.isdir(input):
            self.filelist = [os.path.join(input, f) \
                                for f in os.listdir(input) \
                                if f.endswith(".vm") and os.path.isfile(os.path.join(input, f))]
            outputPath = os.path.join(input, os.path.basename(os.path.normpath(input)) + ".asm")
        elif os.path.isfile(input):
            self.filelist = [input]
            outputPath = os.path.splitext(input)[0] + ".asm"
        else:
            raise ValueError(f"Input must be a file or directory: {input}")
        
        self.parser = Parser(self.filelist[0])
        
        self.codeWriter = CodeWriter(outputPath)

    def translate(self):
        while self.parser.hasMoreLines():

            # parsing
            self.parser.advance()
            # print(self.parser.currentCmd, self.parser.currentCmdType)

            # write
            if self.parser.currentCmdType == CommandType.C_ARITHMETIC:
                self.codeWriter.writeArithmetic(self.parser.arg1())
            
            elif self.parser.currentCmdType in [CommandType.C_PUSH, CommandType.C_POP]:    
                self.codeWriter.writePushPop(self.parser.currentCmdType, 
                                             self.parser.arg1(),
                                             self.parser.arg2())
            elif self.parser.currentCmdType == CommandType.C_LABEL:    
                self.codeWriter.writeLabel(self.parser.arg1())
            elif self.parser.currentCmdType == CommandType.C_IF:    
                self.codeWriter.writeIf(self.parser.arg1())
            elif self.parser.currentCmdType == CommandType.C_GOTO:    
                self.codeWriter.writeGoto(self.parser.arg1())
            elif self.parser.currentCmdType == CommandType.C_FUNCTION:    
                self.codeWriter.writeFunction(self.parser.arg1(), self.parser.arg2())
            elif self.parser.currentCmdType == CommandType.C_RETURN:    
                self.codeWriter.writeReturn()
            elif self.parser.currentCmdType == CommandType.C_CALL:    
                self.codeWriter.writeCall(self.parser.arg1(), self.parser.arg2())
            else:
                raise AssertionError("Unknown Command \"{}\" is detected".format(self.parser.currentCmdType))

def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="path of input file. ex: ./fileName.vm")
    parser.add_argument("--debug", action="store_true", help="run debug mode")
    args = parser.parse_args()
    
    return args

def main(args:argparse.Namespace):
    vmTranslator = VMTranslator(args.input)
    vmTranslator.translate()
    

if __name__ == "__main__":
    args = parser()
    main(args)