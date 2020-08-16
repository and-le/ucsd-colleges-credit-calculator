from .college import College
from .college_constants import *

MARSHALL_PHYS_COURSES = {AP_PHYS_1, AP_PHYS_2, AP_PHYS_MECH, AP_PHYS_EM}
MARSHALL_8_UNIT_BREADTH_COURSES = {AP_DRAW, AP_2D, AP_3D, AP_MUS, AP_US_HIST, AP_EURO_HIST, AP_WORLD_HIST,
                                   AP_CHIN, AP_FREN, AP_GER, AP_ITA, AP_JAP, AP_SPLA, AP_SPLI}

class MarshallCollege(College):

    def __init__(self, name, requirements):
        super().__init__(name, requirements)

    def apply_credits(self, credits):
        for cred in credits:
            for req in self.requirements:
                if cred.course in req.courses:

                    # Only 1 physics credit allowed; skip additional physics credits
                    if (cred.course == AP_PHYS_1) and \
                            (AP_PHYS_2 in req.credits or AP_PHYS_MECH in req.credits or AP_PHYS_EM in req.credits):
                        continue
                    elif (cred.course == AP_PHYS_2) and \
                            (AP_PHYS_1 in req.credits or AP_PHYS_MECH in req.credits or AP_PHYS_EM in req.credits):
                        continue
                    elif (cred.course == AP_PHYS_MECH) and \
                            (AP_PHYS_1 in req.credits or AP_PHYS_2 in req.credits or AP_PHYS_EM in req.credits):
                        continue
                    elif (cred.course == AP_PHYS_EM) and \
                            (AP_PHYS_1 in req.credits or AP_PHYS_2 in req.credits or AP_PHYS_MECH in req.credits):
                        continue

                    # Some AP courses count for 8 units of discplinary breadth
                    elif cred.course in MARSHALL_8_UNIT_BREADTH_COURSES:
                        req.add_credit(cred.course, LARGER_UNIT_QTY)

                    else:
                        req.add_credit(cred.course, BASE_UNIT_QTY)

        # Update the number of credited units
        self.compute_credited_units()