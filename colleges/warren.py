from .college import College
from .college_constants import *

# Warren College constants
POFC = "PofC"
AREA_STUDY = "AS"

POFC_HUM = "Humanities and Fine Arts"
POFC_SCI = "Math and Natural Sciences and Engineering"
POFC_SOC = "Social Sciences"

AREA_STUDY_HUM = "Humanities and Fine Arts"
AREA_STUDY_SOC = "Social Sciences"


class WarrenCollege(College):

    def __init__(self, name, requirements, pofc, area_studies):
        super().__init__(name, requirements)
        self.pofc = pofc
        self.area_studies = area_studies

        self.gen_unit_total = 0
        self.pofc_unit_total = 0
        self.area_study_unit_total = 0

        self.gen_credited_units = 0
        self.pofc_credited_units = 0
        self.area_study_credited_units = 0

        # There are 3 different PofC. 2 are chosen at a time, so there are 3 different combinations.
        self.pofc_hum = None
        self.pofc_soc = None
        self.pofc_sci = None

        # There are 2 different AS
        self.area_study_hum = None
        self.area_study_soc = None

        for r in requirements:
            if r.name == POFC:
                self.pofc_unit_total += r.unit_total
            elif r.name == AREA_STUDY:
                self.area_study_unit_total += r.unit_total
            else:
                self.gen_unit_total += r.unit_total

    def apply_credits(self, credits):
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
                                pofc.add_credit(cred.course, BASE_UNIT_QTY)


                    # If the requirement is an AS
                    elif req.name == AREA_STUDY:
                        # Iterate over the AS
                        for area_study in self.area_studies:
                            # If the AP credit fulfills the PofC
                            if cred.course in area_study.courses:
                                area_study.add_credit(cred.course, BASE_UNIT_QTY)

                    # If the requirement is *not* a PofC or AS
                    else:
                        req.add_credit(cred.course, BASE_UNIT_QTY)


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

                    # Update the best choices
        self.pofc_hum, self.pofc_soc, self.pofc_sci = best_hum_pofc, best_soc_pofc, best_sci_pofc
        self.area_study_hum, self.area_study_soc = best_hum_area_study, best_soc_area_study

        # Update the number of credited units (doesn't update for PofC and Area Studies)
        self.compute_credited_units()

    def compute_credited_units(self):
        # Update only non-PofC and non-AS requirements
        for req in self.requirements:
            if req.name != POFC and req.name != AREA_STUDY:
                self.gen_credited_units += req.credit_units

    def get_pofc_unit_total(self):
        return self.pofc_unit_total

    def get_area_study_unit_total(self):
        return self.area_study_unit_total

    def get_gen_unit_total(self):
        return self.gen_unit_total

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