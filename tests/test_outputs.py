from pathlib import Path
from main import main

def test_main_writes_txt(tmp_path: Path):
    out = tmp_path / "report.txt"
    code = main(["--text", "ola ola mundo", "--out", str(out), "--n", "2"])
    assert code == 0
    assert out.exists()
    assert "ola" in out.read_text(encoding="utf-8").lower()

def test_main_writes_csv(tmp_path: Path):
    out = tmp_path / "report.txt"
    code = main(["--text", "ola ola mundo", "--out", str(out), "--csv", "--n", "2"])
    assert code == 0
    csv_path = out.with_suffix(".csv")
    assert csv_path.exists()
    content = csv_path.read_text(encoding="utf-8").lower()
    assert "word" in content and "count" in content