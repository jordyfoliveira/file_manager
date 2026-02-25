@echo off
python -m pip install -r requirements-dev.txt
python -m pytest -q --cov=. --cov-report=term-missing