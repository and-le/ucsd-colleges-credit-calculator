from .college import College
from .ap_constants import *


ROOSEVELT_8_UNIT_SCIENCE_COURSES = {AP_BIO, AP_CHEM, AP_PHYS_1, AP_PHYS_2}

class RooseveltCollege(College):

    def __init__(self, name, requirements):
        super().__init__(name, requirements)

    def apply_credits(self, credits):
        """
        The rules for determining credit for Roosevelt are simpler than some of the other colleges.
        The only special cases are for certain science courses: these ones count for 8 units rather than 4.
        :param credits:
        :return:
        """
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