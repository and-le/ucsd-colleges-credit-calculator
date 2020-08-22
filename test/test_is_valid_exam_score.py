import unittest

from src.is_valid_exam_score import is_valid_exam_score

class ExamScoreTestCase(unittest.TestCase):
    def test_invalid_score_string(self):
        score = "Not a valid score"
        self.assertFalse(is_valid_exam_score(score))

    def test_invalid_score_integer(self):
        score = "10"
        self.assertFalse(is_valid_exam_score(score))

    def test_valid_score(self):
        for i in range(1, 6):
            self.assertTrue(is_valid_exam_score(str(i)))

if __name__ == '__main__':
    unittest.main()
