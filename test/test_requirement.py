import unittest
from src.requirements import Requirement

class RequirementTestCase(unittest.TestCase):
    def test_exceeding_units(self):
        name = "Revelle Social Science"
        unit_total = 8
        unit_limit = 8
        courses = ["AP Comparative Government and Politics",
                   "AP United States Government and Politics",
                   "AP United States History",
                   "AP Psychology"]
        req = Requirement(name, unit_total, unit_limit, courses)

        req.add_credit("AP Comparative Government and Politics", 4)
        req.add_credit("AP United States Government Politics", 4)
        # Course and its credits should not be added because it exceeds the unit requirement
        req.add_credit("AP United States History Government and Politics", 4)

        expected = 8
        self.assertEqual(expected, req.credit_units)

if __name__ == '__main__':
    unittest.main()
