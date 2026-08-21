# Define Python version and path variables
PYTHON_VERSION = 3.10.5

choco:
	@echo "Installing packages with Chocolatey"choco upgrade chocolatey
	@powershell  -Command "make Install-Package"
	@echo "All packages installed."

# Installation and configuration commands
python-setup:
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
	choco install wget -y --force; \
	Write-Host \"Package installation complete.\";"
