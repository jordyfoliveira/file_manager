## Como correr
```bash
python app.py --text "ola mundo mundo" --n 5
python app.py --input input.txt --n 10 --out output/report.txt --csv# file_manager


### 3) (Opcional mas excelente) criar um script “1-click”
No Windows, cria `run_tests.bat`:
```bat
@echo off
python -m pip install -r requirements-dev.txt
python -m pytest -q