import os
from common.commandType import CommandType
class Parser:
    def __init__(self, inputFile:str):
        self.fileHandle = open(inputFile, "r", encoding="utf-8")
        self.fileSize = os.path.getsize(inputFile)
        self.currentCmd = None
        self.currentCmdType = None
    
    def __del__(self):
        self.fileHandle.close()

    def hasMoreLines(self)->bool:
        if self.fileHandle.tell() < self.fileSize:
            ret = True
        else:
            ret = False

        return ret

    def advance(self):
        while 1:
            self.currentCmd = self.fileHandle.readline().rstrip("\n")
            self.currentCmd = self.__stripLeadingTabs(self.currentCmd)
            if self.__isCommand():
                self.currentCmdType = self.commandType()
                break

    
    def commandType(self) -> CommandType:
        assert self.currentCmd, "This method cannot be used if the current command type is empty"

        if self.currentCmd.split(" ")[0] in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return CommandType.C_ARITHMETIC
        elif self.currentCmd.split(" ")[0] == "push":
            return CommandType.C_PUSH
        elif self.currentCmd.split(" ")[0] == "pop":
            return CommandType.C_POP
        elif self.currentCmd.split(" ")[0] == "label":
            return CommandType.C_LABEL
        else:
            raise AssertionError("An unknown command type:{!r} was read.".format(self.currentCmd))
        
    def arg1(self) -> str:
        assert self.currentCmdType != CommandType.C_RETURN, \
            "This method cannot be used if the current command type is C_RETURN.\n \
                current command is {}".format(self.currentCmd)
        if self.currentCmdType == CommandType.C_ARITHMETIC:
            return self.currentCmd
        elif self.currentCmdType in [CommandType.C_PUSH, CommandType.C_POP, CommandType.C_LABEL]:
            return self.currentCmd.split(" ")[1]
        else:
            raise AssertionError("An unknown command type was read.")

    def arg2(self) -> int:
        assert self.currentCmdType in [CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL], \
            "This method cannot be used if the current command type is not C_PUSH, C_POP, C_FUNCTION."
        if self.currentCmdType == CommandType.C_PUSH:
            return self.currentCmd.split(" ")[2]
        elif self.currentCmdType == CommandType.C_POP:
            return self.currentCmd.split(" ")[2]
        else:
            raise AssertionError("An unknown command type was read.")
    
    def __isCommand(self) -> bool:

        if self.currentCmd.startswith("//") or self.currentCmd == "":
            return False
        else:
            return True
        
    def __stripLeadingTabs(self, cmd: str) -> str:

        if cmd.startswith("\t"):
            return cmd.lstrip("\t")
        else:
            return cmd
