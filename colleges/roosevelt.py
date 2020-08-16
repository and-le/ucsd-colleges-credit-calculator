from .college import College
from .college_constants import *


ROOSEVELT_8_UNIT_SCIENCE_COURSES = {AP_BIO, AP_CHEM, AP_PHYS_1, AP_PHYS_2}


class RooseveltCollege(College):

    def __init__(self, name, requirements):
        super().__init__(name, requirements)

    def apply_credits(self, credits):
        for cred in credits:
            for req in self.requirements:
                if cred.course in req.courses:

                    # Special cases: AP Biology, Chemistry, Physics 1, Physics 2 are 8 units
                    if cred.course in ROOSEVELT_8_UNIT_SCIENCE_COURSES:
                        # Clear out any potential 4-unit courses
                        req.clear_credits()
                        req.add_credit(cred.course, LARGER_UNIT_QTY)

                    else:
                        req.add_credit(cred.course, BASE_UNIT_QTY)

        # Update the number of credited units
        self.compute_credited_units()