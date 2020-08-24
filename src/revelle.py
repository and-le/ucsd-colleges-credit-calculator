from .college import College
from.ap_constants import *

# Courses that need a score of 4 to count for applied credit
REVELLE_SCORE_OF_FOUR_COURSES = [AP_CALC_AB, AP_CALC_BC, AP_CHIN, AP_FREN, AP_GER, AP_ITA, AP_JAP, AP_SPLA]

# Courses that need a score of 5 to count for applied credit
REVELLE_SCORE_OF_FIVE_COURSES = [AP_CHEM]


class RevelleCollege(College):
    def __init__(self, name, requirements):
        super().__init__(name, requirements)

    def apply_credits(self, credits):
        """
        Revelle College has simpler rules for determining credit than some of the other
        src. The general process for applying credit is shown in this method.
        :param credits: List of AP Credits
        :return:
        """
        # Reset credited units
        self.credited_units = 0

        # Iterate over the AP Credits
        for cred in credits:
            # Iterate over the college's requirements
            for req in self.requirements:
                # If this AP course fulfills a college requirement + has a score higher than 3, the minimum for credit
                # to be applied
                if cred.course in req.courses and cred.score >= AP_SCORE_3:
                    # Check for score requirements

                    if cred.course in REVELLE_SCORE_OF_FOUR_COURSES:
                        if cred.score >= AP_SCORE_4:
                            if cred.course == AP_CALC_BC:
                                # Reset the credit limit, because the limit is 8 and 8 units need to be added
                                req.clear_credits()
                                req.add_credit(cred.course, EIGHT_UNITS)
                            else:
                                req.add_credit(cred.course, FOUR_UNITS)
                        # Score is < 4
                        else:
                            continue

                    elif cred.course in REVELLE_SCORE_OF_FIVE_COURSES:
                        if cred.score == AP_SCORE_5:
                            req.add_credit(cred.course, FOUR_UNITS)
                        # Score is < 5
                        else:
                            continue

                    # Any exam that requires a minimum score of 3
                    else:
                        req.add_credit(cred.course, FOUR_UNITS)

        # Update the number of credited units
        self.compute_credited_units()
