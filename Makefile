-include .env
export

# Define Python version and path variables
PYTHON_VERSION = 3.11.6
OPENSSL_LIB=C:\ProgramData\chocolatey\lib\openssl\lib
OPENSSL_INCLUDE=C:\ProgramData\chocolatey\lib\openssl\include


choco:
	@echo "Installing packages with Chocolatey"choco upgrade chocolatey
	@powershell  -Command "make Install-Package"
	@echo "All packages installed."
	@powershell -Command "pip install pre-commit"

# Installation and configuration commands
python-setup:
	@set "LDFLAGS=-L$(OPENSSL_LIB)"
	@set "CPPFLAGS=-I$(OPENSSL_INCLUDE)"
	@pyenv update
	@pyenv install $(PYTHON_VERSION)
	@pyenv local $(PYTHON_VERSION)
	@echo "Python $(PYTHON_VERSION) installed and set locally."

reqs:
	@call.venv\Scripts\activate && python -m pip install --upgrade pip setuptools wheel
	@call.venv\Scripts\activate && python -m pip install -r requirements.txt
	@echo "======================="
	@echo "Virtual environment successfully created with requirements installed"
	@echo "To activate the venv type '.venv\Scripts\activate'"

venv:
	@python3 -m venv .venv
	@echo "Virtual environment '.venv' created."
	@make reqs

.PHONY: Install-Package

Install-Package:
	@powershell -NoProfile -ExecutionPolicy Bypass -Command \
	"choco install pyenv-win -y --force; \
	choco install openssl -y --force; \
	choco install sqlite -y --force; \
	Write-Host \"Package installation complete.\";"
