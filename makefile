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
	@echo "Running Python script using virtual environment..."
	$(EXECUTABLE) fileName.vm

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

$(EXECUTABLE): VMTranslator.py
	@echo "#!$(PYTHON)" > $(EXECUTABLE)
	@cat VMTranslator.py >> $(EXECUTABLE)
	@chmod +x $(EXECUTABLE)

update:
	$(PYTHON) -m pip install --upgrade -r requirements.txt

clean:
	$(RM) $(VENV_DIR)
	$(RM) $(EXECUTABLE)

.PHONY: activate run clean