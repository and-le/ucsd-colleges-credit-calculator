from .college import College
from.ap_constants import FOUR_UNITS


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
        # Iterate over the AP Credits
        for cred in credits:
            # Iterate over the college's requirements
            for req in self.requirements:
                # If this AP course fulfills a college requirement
                if cred.course in req.courses:
                    req.add_credit(cred.course, FOUR_UNITS)

        # Update the number of credited units
        self.compute_credited_units()
