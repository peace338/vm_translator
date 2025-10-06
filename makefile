VENV_DIR := .venv

ifeq ($(OS),Windows_NT)
	PYTHON := $(VENV_DIR)/Scripts/python.exe
	ACTIVATE := $(VENV_DIR)/Scripts/activate
	RM := rmdir /s /q
else
	PYTHON := $(VENV_DIR)/bin/python
	ACTIVATE := $(VENV_DIR)/bin/activate
	RM := rm -rf
endif

$(info PYTHON = $(PYTHON))
run: $(VENV_DIR)/setup activate VMTranslator
	@echo "Running Python script using virtual environment..."
	VMTranslator fileName.vm

$(VENV_DIR)/setup: requirements.txt
	@echo "Creating virtual environment..."
	python -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Virtual environment setup complete."
	@touch $(VENV_DIR)/setup

activate:
	@echo "To activate the virtual environment, run:"
ifeq ($(OS),Windows_NT)
	@echo "$(ACTIVATE)"
else
	@echo "source $(ACTIVATE)"
endif

VMTranslator: VMTranslator.py
	@echo "#!$(PYTHON)" > VMTranslator
	@cat VMTranslator.py >> VMTranslator
	@chmod +x VMTranslator

update:
	$(PYTHON) -m pip install --upgrade -r requirements.txt

clean:
	$(RM) $(VENV_DIR)

.PHONY: activate run clean