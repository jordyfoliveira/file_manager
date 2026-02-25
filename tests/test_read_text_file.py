from pathlib import Path
from app import read_text_file

def test_read_text_file_utf8(tmp_path: Path):
    p = tmp_path / "a.txt"
    p.write_text("olá mundo", encoding="utf-8")

    text = read_text_file(str(p))
    assert "olá" in text

def test_read_text_file_latin1_fallback(tmp_path: Path):
    p = tmp_path / "b.txt"
    p.write_text("olá mundo", encoding="latin-1")

    text = read_text_file(str(p))
    assert "olá" in text

def test_read_text_file_not_found(tmp_path: Path):
    p = tmp_path / "nao_existe.txt"
    text = read_text_file(str(p))
    assert text == ""