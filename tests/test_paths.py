from pathlib import Path
from file_manager import ensure_txt_path

def test_ensure_txt_path_directory(tmp_path: Path):
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    result = ensure_txt_path(out_dir)
    assert result == out_dir / "report.txt"

def test_ensure_txt_path_file(tmp_path: Path):
    out_file = tmp_path / "my_report.txt"
    result = ensure_txt_path(out_file)
    assert result == out_file