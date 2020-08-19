from .college import College
from .ap_constants import *

# Warren College constants
POFC = "PofC"
AREA_STUDY = "AS"

POFC_HUM = "Humanities and Fine Arts"
POFC_SCI = "Math and Natural Sciences and Engineering"
POFC_SOC = "Social Sciences"

AREA_STUDY_HUM = "Humanities and Fine Arts"
AREA_STUDY_SOC = "Social Sciences"

# In general, Warren PofC credits count for 8 units. Some, however, only count for 4.
WARREN_POFC_FOUR_UNIT_COURSES = {AP_MACRO, AP_MICRO, AP_ENV, AP_US_GOV, AP_COMP_GOV, AP_LAT,
                                 AP_PHYS_MECH, AP_PHYS_EM, AP_PSY}

# There is a 12-unit limit on the amount of credit units that can be applied to PofC.
# Some PofC categories credit 8 units for each AP Exam. If students have 2 or more
# qualifying credits for these PofC, then the maximum number of units they can earn is 12.
WARREN_POFC_VIS_ARTS_COURSES = {AP_DRAW, AP_2D, AP_3D, AP_ART_HIST}
WARREN_POFC_HIST_COURSES = {AP_WORLD_HIST, AP_US_HIST, AP_EURO_HIST}
# Since Foreign Language credits are a subset of Literature credits, Literature credits will always take
# precedence when determining which Program of Concentration yields the most units.
WARREN_POFC_LIT_COURSES = {AP_ENG_LANG, AP_ENG_LIT, AP_LAT, AP_SPLA, AP_SPLI, AP_GER, AP_ITA, AP_FREN, AP_CHEM, AP_JAP}
WARREN_POFC_LANG_COURSES = {AP_SPLA, AP_SPLI, AP_GER, AP_ITA, AP_FREN, AP_CHEM, AP_JAP}

WARREN_VIS_ART_POFC_NAME = "Visual Arts"
WARREN_HIST_POFC_NAME = "History"
WARREN_LIT_POFC_NAME = "Literature"
WARREN_LANG_POFC_NAME = "Foreign Language and Culture"


class WarrenCollege(College):

    def __init__(self, name, requirements, pofc, area_studies):
        super().__init__(name, requirements)
        self.pofc = pofc
        self.area_studies = area_studies

        self.gen_unit_total = 0
        self.gen_credited_units = 0

        self.pofc_unit_total = 0
        # There are 3 different PofC. 2 are chosen at a time, so there are 3 different combinations:
        # 1. HUM + SOC
        # 2. HUM + SCI
        # 3. SOC + SCI
        self.pofc_hum = None
        self.pofc_soc = None
        self.pofc_sci = None
        self.pofc_hum_soc_credited_units = 0
        self.pofc_hum_sci_credited_units = 0
        self.pofc_soc_sci_credited_units = 0

        self.area_study_unit_total = 0
        # There are 2 different AS
        self.area_study_hum = None
        self.area_study_hum_credited_units = 0
        self.area_study_soc = None
        self.area_study_soc_credited_units = 0


        for r in requirements:
            if r.name == POFC:
                self.pofc_unit_total += r.unit_total
            elif r.name == AREA_STUDY:
                self.area_study_unit_total += r.unit_total
            else:
                self.gen_unit_total += r.unit_total

    def apply_credits(self, credits):
        """
        Warren has the most complex rules for determining credit. First, students have different unit requirements
        depending on whether they must complete Programs of Concentration or Area Studies. Furthermore, there are 3
        different categories for Programs of Concentration, and students must choose the 2 that do not overlap
        with their major. This method considers both Programs of Concentration and Area Studies, as well as
        all 3 combinations of Programs of Concentration choices.
        :param credits:
        :return:
        """
        # Iterate over the AP Credits
        for cred in credits:
            # Iterate over the college reqs
            for req in self.requirements:
                # If the AP Credit fulfills a college requirement
                if cred.course in req.courses:

                    # If the requirement is a PofC
                    if req.name == POFC:
                        # Iterate over the PofC
                        for pofc in self.pofc:
                            # If the AP credit fulfills the PofC
                            if cred.course in pofc.courses:

                                if cred.course in WARREN_POFC_FOUR_UNIT_COURSES:
                                    pofc.add_credit(cred.course, FOUR_UNITS)

                                else:
                                    # If a course belongs to a PofC for which there are multiple 8-unit credits
                                    # and the current PofC is such a PofC
                                    if pofc.name == WARREN_VIS_ART_POFC_NAME and cred.course in WARREN_POFC_VIS_ARTS_COURSES:
                                        # If a credit was already applied
                                        if pofc.credits:
                                            # Add 4 units to meet the unit limit
                                            pofc.add_credit(cred.course, FOUR_UNITS)
                                        else:
                                            pofc.add_credit(cred.course, EIGHT_UNITS)

                                    elif pofc.name == WARREN_HIST_POFC_NAME and cred.course in WARREN_POFC_HIST_COURSES:
                                        if pofc.credits:
                                            pofc.add_credit(cred.course, FOUR_UNITS)
                                        else:
                                            pofc.add_credit(cred.course, EIGHT_UNITS)

                                    elif pofc.name == WARREN_LIT_POFC_NAME and cred.course in WARREN_POFC_LIT_COURSES:
                                        if pofc.credits:
                                            pofc.add_credit(cred.course, FOUR_UNITS)
                                        else:
                                            pofc.add_credit(cred.course, EIGHT_UNITS)

                                    elif pofc.name == WARREN_LANG_POFC_NAME and cred.course in WARREN_POFC_LANG_COURSES:
                                        if pofc.credits:
                                            pofc.add_credit(cred.course, FOUR_UNITS)
                                        else:
                                            pofc.add_credit(cred.course, EIGHT_UNITS)

                                    # Course doesn't belong to a PofC for which there are multiple 8-unit credits
                                    else:
                                        pofc.add_credit(cred.course, EIGHT_UNITS)

                    # If the requirement is an AS
                    elif req.name == AREA_STUDY:
                        # Iterate over the AS
                        for area_study in self.area_studies:
                            # If the AP credit fulfills the PofC
                            if cred.course in area_study.courses:
                                area_study.add_credit(cred.course, FOUR_UNITS)

                    # If the requirement is *not* a PofC or AS
                    else:
                        req.add_credit(cred.course, FOUR_UNITS)

        self.compute_best_pofc()
        self.compute_best_as()

        # Update the number of credited units
        self.compute_credited_units()

    def compute_best_pofc(self):
        # Select the PofCs that maximize the amount of applied credits
        best_hum_pofc = best_soc_pofc = best_sci_pofc = None
        for pofc in self.pofc:
            if pofc.category == POFC_HUM:
                # Initialize humanities PofC
                if not best_hum_pofc:
                    best_hum_pofc = pofc
                elif pofc.credit_units > best_hum_pofc.credit_units:
                    best_hum_pofc = pofc
            elif pofc.category == POFC_SOC:
                # Initialize social PofC
                if not best_soc_pofc:
                    best_soc_pofc = pofc
                elif pofc.credit_units > best_soc_pofc.credit_units:
                    best_soc_pofc = pofc
            elif pofc.category == POFC_SCI:
                # Initialize science PofC
                if not best_sci_pofc:
                    best_sci_pofc = pofc
                elif pofc.credit_units > best_sci_pofc.credit_units:
                    best_sci_pofc = pofc

        self.pofc_hum, self.pofc_soc, self.pofc_sci = best_hum_pofc, best_soc_pofc, best_sci_pofc

    def compute_best_as(self):
        # Select the Area Studies that maximize the amount of applied credits
        best_hum_area_study = best_soc_area_study = None
        for area_study in self.area_studies:
            if area_study.category == AREA_STUDY_HUM:
                # Initialize humanities AS
                if not best_hum_area_study:
                    best_hum_area_study = area_study
                elif area_study.credit_units > best_hum_area_study.credit_units:
                    best_hum_area_study = area_study
            elif area_study.category == AREA_STUDY_SOC:
                # Initialize social AS
                if not best_soc_area_study:
                    best_soc_area_study = area_study
                elif area_study.credit_units > best_soc_area_study.credit_units:
                    best_soc_area_study = area_study

        self.area_study_hum, self.area_study_soc = best_hum_area_study, best_soc_area_study
        self.area_study_hum.credit_units = best_hum_area_study.credit_units
        self.area_study_soc.credit_units = best_soc_area_study.credit_units

    def compute_credited_units(self):
        for req in self.requirements:
            if req.name == POFC:
                # Update the credit units for all 3 combinations of PofC
                self.pofc_hum_soc_credited_units = self.pofc_hum.credit_units + self.pofc_soc.credit_units
                self.pofc_hum_sci_credited_units = self.pofc_hum.credit_units + self.pofc_sci.credit_units
                self.pofc_soc_sci_credited_units = self.pofc_soc.credit_units + self.pofc_sci.credit_units
            elif req.name == AREA_STUDY:
                self.area_study_hum_credited_units = self.area_study_hum.credit_units
                self.area_study_soc_credited_units = self.area_study_soc.credit_units
            else:
                self.gen_credited_units += req.credit_units

    def get_pofc(self, name):
        """
        Returns the PofC Requirement with the given name.
        :param: name: the name of the PofC to get
        :return: the PofC Requirement with the given name; None if no such PofC exists.
        """
        for pofc in self.pofc:
            if name == pofc.name:
                return pofc

        return None

    def get_pofc_unit_total(self):
        return self.pofc_unit_total

    def get_area_study_unit_total(self):
        return self.area_study_unit_total

    def get_gen_unit_total(self):
        return self.gen_unit_total

    # Warren College has several different unit totals. Conseuqently, methods
    # that report a singular unit total don't make sense for Warren.

    def compute_unit_total(self, requirements):
        """
        Not implemented, but super-class constructor calls this method, so a NotImplementedError cannot be raised
        :param requirements:
        :return:
        """
        pass

    def get_unit_total(self):
        raise NotImplementedError()

    def get_credited_units(self):
        raise NotImplementedError()

    def get_net_units(self):
        raise NotImplementedError()

    def display_gen_results(self):
        print(f"Non-PofC and Non-Area-Study Credits:\n")
        for req in self.requirements:
            if req.name != POFC and req.name != AREA_STUDY:
                print(f"{req.name} - Applied Credits:")
                for cred in req.credits:
                    print(cred)
        print()

    def display_pofc_hum(self):
        # Only display the PofC if any credits were actually applied
        if self.pofc_hum.credit_units > 0:
            print(f"Humanities and Fine Arts PofC: {self.pofc_hum.name}")
            for cred in self.pofc_hum.credits:
                print(cred)
        else:
            print(f"Humanities and Fine Arts PofC: No Credits Applied")

    def display_pofc_soc(self):
        # Only display the PofC if any credits were actually applied
        if self.pofc_soc.credit_units > 0:
            print(f"Social Sciences PofC: {self.pofc_soc.name}")
            for cred in self.pofc_soc.credits:
                print(cred)
        else:
            print(f"Social Sciences PofC: No Credits Applied")

    def display_pofc_sci(self):
        # Only display the PofC if any credits were actually applied
        if self.pofc_sci.credit_units > 0:
            print(f"Math and Natural Sciences and Engineering PofC: {self.pofc_sci.name}")
            for cred in self.pofc_sci.credits:
                print(cred)
        else:
            print(f"Social Sciences PofC: No Credits Applied")

    def display_area_study_hum(self):
        if self.area_study_hum.credit_units > 0:
            print(f"Humanities and Fine Arts Area Study: {self.area_study_hum.name}")
            for cred in self.area_study_hum.credits:
                print(cred)
        else:
            print(f"Humanities and Fine Arts Area Study: No Credits Applied")

    def display_area_study_soc(self):
        if self.area_study_soc.credit_units > 0:
            print(f"Social Sciences Area Study: {self.area_study_soc.name}")
            for cred in self.area_study_soc.credits:
                print(cred)
        else:
            print(f"Social Sciences Area Study: No Credits Applied")

    def display_pofc_results(self):
        print(f"Non-engineering majors must complete Programs of Concentration (PofC):")
        pofc_total = self.get_pofc_unit_total() + self.get_gen_unit_total()
        print(f"{self} has a total of {pofc_total} units if your major requires POFC.")

        print(f"There are 3 different combinations of PofC:\n")
        print(f"1) Humanities and Fine Arts + Social Sciences")
        print(f"2) Humanities and Fine Arts + Math and Natural Sciences and Engineering")
        print(f"3) Social Sciences + Math and Natural Sciences and Engineering\n")

        print(f"The following AP Courses were used toward 1) Humanities and Fine Arts + Social Sciences:")
        self.display_pofc_hum()
        self.display_pofc_soc()
        hum_soc_units = pofc_total - (self.pofc_hum.credit_units + self.pofc_soc.credit_units) - self.gen_credited_units
        print(f"\nAfter applying AP Credit, the remaining amount of units is {hum_soc_units}\n")

        print(
            f"The following AP Courses were used toward 2) Humanities and Fine Arts + Math and Natural Sciences and Engineering")
        self.display_pofc_hum()
        self.display_pofc_sci()
        hum_sci_units = pofc_total - (self.pofc_hum.credit_units + self.pofc_sci.credit_units) - self.gen_credited_units
        print(f"\nAfter applying AP Credit, the remaining amount of units is {hum_sci_units}\n")

        print(
            f"The following AP Courses were used toward 3) Social Sciences + Math and Natural Sciences and Engineering")
        self.display_pofc_soc()
        self.display_pofc_sci()
        soc_sci_units = pofc_total - (self.pofc_soc.credit_units + self.pofc_sci.credit_units) - self.gen_credited_units
        print(f"\nAfter applying AP Credit, the remaining amount of units is {soc_sci_units}")

    def display_as_results(self):
        print(f"Engineering majors must complete Area Studies (AS):")
        as_total = self.get_area_study_unit_total() + self.get_gen_unit_total()
        print(f"{self} has a total of {as_total} units if your major requires Area Studies.\n")

        print(f"There are 2 Area Studies:\n")
        print(f"1) Humanities and Fine Arts")
        print(f"2) Social Sciences\n")

        print(f"The following AP Courses were used toward 1) Humanities and Fine Arts:")
        self.display_area_study_hum()

        print(f"\nThe following AP Courses were used toward 2) Social Sciences:")
        self.display_area_study_soc()

        rem_units = as_total - (self.area_study_hum.credit_units + self.area_study_soc.credit_units) - self.gen_credited_units
        print(f"\nAfter applying AP Credit, the remaining amount of units is {rem_units}.")

    def display_results(self):
        print(f"Results for {self.name}:\n")

        self.display_gen_results()
        print()
        self.display_pofc_results()
        print()
        self.display_as_results()