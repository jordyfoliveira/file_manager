import unittest
from text_analysis import top_words

class TestTextAnalysis(unittest.TestCase):
    def test_punctuation_split(self):
        self.assertEqual(top_words("ola!!!ola", 5), [("ola", 2)])

    def test_tie_break_alpha(self):
        # a e b aparecem 2 vezes, deve ordenar alfabeticamente no empate
        self.assertEqual(top_words("b a b a c", 3), [("a", 2), ("b", 2), ("c", 1)])

    def test_accents_normalization(self):
        # "Olá" e "ola" devem contar como a mesma palavra ("ola")
        self.assertEqual(top_words("Olá ola OLÁ", 1), [("ola", 3)])

if __name__ == "__main__":
    unittest.main()