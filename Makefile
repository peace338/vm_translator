VENV_DIR := .venv
EXECUTABLE := ./VMTranslator

ifeq ($(OS),Windows_NT)
	PYTHON := $(VENV_DIR)/Scripts/python.exe
	ACTIVATE := $(VENV_DIR)/Scripts/activate
	RM := rmdir /s /q
else
	PYTHON := $(VENV_DIR)/bin/python
	ACTIVATE := $(VENV_DIR)/bin/activate
	RM := rm -rf
endif

run: $(EXECUTABLE)
	@echo "======================================================="
	@echo "= Running Python script using virtual environment..."
	@echo "======================================================="
	$(EXECUTABLE) data/7/MemoryAccess/BasicTest/BasicTest.vm
	$(EXECUTABLE) data/7/MemoryAccess/PointerTest/PointerTest.vm
	$(EXECUTABLE) data/7/MemoryAccess/StaticTest/StaticTest.vm
	$(EXECUTABLE) data/7/StackArithmetic/SimpleAdd/SimpleAdd.vm
	$(EXECUTABLE) data/7/StackArithmetic/StackTest/StackTest.vm

$(EXECUTABLE): VMTranslator.py
	@echo "#!$(PYTHON)" > $(EXECUTABLE)
	@cat VMTranslator.py >> $(EXECUTABLE)
	@chmod +x $(EXECUTABLE)

clean:
	$(RM) $(VENV_DIR)
	$(RM) $(EXECUTABLE)

test: run
	@echo "======================================================="
	@echo "= Testing..."
	@echo "======================================================="
	CPUEmulator.sh data/7/MemoryAccess/BasicTest/BasicTest.tst
	CPUEmulator.sh data/7/MemoryAccess/PointerTest/PointerTest.tst
	CPUEmulator.sh data/7/MemoryAccess/StaticTest/StaticTest.tst
	CPUEmulator.sh data/7/StackArithmetic/SimpleAdd/SimpleAdd.tst
	CPUEmulator.sh data/7/StackArithmetic/StackTest/StackTest.tst

.PHONY: activate run clean test