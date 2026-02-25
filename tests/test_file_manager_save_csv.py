import unittest
from pathlib import Path
import tempfile

from app import save_csv  # importa do teu app.py

class TestSaveCSV(unittest.TestCase):
    def test_save_csv_creates_expected_file(self):
        items = [("ola", 2), ("mundo", 1)]

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "report.csv"

            save_csv(items, out_path)

            self.assertTrue(out_path.exists())

            content = out_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(content[0], "rank,word,count")
            self.assertEqual(content[1], "1,ola,2")
            self.assertEqual(content[2], "2,mundo,1")

if __name__ == "__main__":
    unittest.main()