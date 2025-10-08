VENV_DIR := .venv
EXECUTABLE := VMTranslator

ifeq ($(OS),Windows_NT)
	PYTHON := $(VENV_DIR)/Scripts/python.exe
	ACTIVATE := $(VENV_DIR)/Scripts/activate
	RM := rmdir /s /q
else
	PYTHON := $(VENV_DIR)/bin/python
	ACTIVATE := $(VENV_DIR)/bin/activate
	RM := rm -rf
endif

run: $(VENV_DIR)/setup activate $(EXECUTABLE)
	@echo "======================================================="
	@echo "= Running Python script using virtual environment..."
	@echo "======================================================="
	$(EXECUTABLE) data/7/MemoryAccess/BasicTest/BasicTest.vm
# 	$(EXECUTABLE) data/7/MemoryAccess/PointerTest/PointerTest.vm
# 	$(EXECUTABLE) data/7/MemoryAccess/StaticTest/StaticTest.vm
	$(EXECUTABLE) data/7/StackArithmetic/SimpleAdd/SimpleAdd.vm
	$(EXECUTABLE) data/7/StackArithmetic/StackTest/StackTest.vm

$(VENV_DIR)/created: requirements.txt
	@echo "Creating virtual environment..."
	python -m venv $(VENV_DIR)
	@touch $(VENV_DIR)/created

activate: $(VENV_DIR)
	@echo "To activate the virtual environment, run:"
ifeq ($(OS),Windows_NT)
	@echo "$(ACTIVATE)"
else
	@echo "source $(ACTIVATE)"
endif

$(EXECUTABLE): VMTranslator.py
	@echo "#!$(PYTHON)" > $(EXECUTABLE)
	@cat VMTranslator.py >> $(EXECUTABLE)
	@chmod +x $(EXECUTABLE)

$(VENV_DIR)/setup: requirements.txt | $(VENV_DIR)/created
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Virtual environment setup complete."
	@touch $(VENV_DIR)/setup

clean:
	$(RM) $(VENV_DIR)
	$(RM) $(EXECUTABLE)

test: run
	@echo "======================================================="
	@echo "= Testing..."
	@echo "======================================================="
	CPUEmulator data/7/MemoryAccess/BasicTest/BasicTest.tst
# 	CPUEmulator data/7/MemoryAccess/PointerTest/PointerTest.tst
# 	CPUEmulator data/7/MemoryAccess/StaticTest/StaticTest.tst
	CPUEmulator data/7/StackArithmetic/SimpleAdd/SimpleAdd.tst
	CPUEmulator data/7/StackArithmetic/StackTest/StackTest.tst

.PHONY: activate run clean test