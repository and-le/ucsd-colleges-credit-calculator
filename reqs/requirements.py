import csv
from .requirement_constants import *

class APCredit:

    def __init__(self, course, score):
        self.course = course
        self.score = score

    def __repr__(self):
        return f"Course: {self.course} - Exam score: {self.score}"


class Requirement:

    def __init__(self, name, unit_total, unit_limit, courses):
        self.name = name
        self.unit_total = unit_total
        self.unit_limit = unit_limit
        self.courses = courses

        self.credits = set()
        self.credit_units = 0

    def __repr__(self):
        return f"{self.name} - Unit total: {self.unit_total} - Unit limit: {self.unit_limit} - Courses: {self.courses}"

    def add_credit(self, credit, units, ignore_limit=False):
        if not ignore_limit:
            if self.credit_units + units <= self.unit_limit:
                self.credits.add(credit)
                self.credit_units += units
        else:
            self.credits.add(credit)
            self.credit_units += units

    def clear_credits(self):
        self.credits.clear()
        self.credit_units = 0


class SubRequirement(Requirement):
    def __init__(self, name, unit_total, unit_limit, courses, parent_requirement):
        super().__init__(name, unit_total, unit_limit, courses)
        self.parent_requirement = parent_requirement

    def __repr__(self):
        return f"Parent: {self.parent_requirement.name} - SubRequirement: {self.name} - Courses: {self.courses}"


class WarrenSubRequirement(SubRequirement):
    def __init__(self, name, unit_total, unit_limit, courses, parent_requirement, category):
        super().__init__(name, unit_total, unit_limit, courses, parent_requirement)
        self.parent_requirement = parent_requirement
        self.category = category

    def __repr__(self):
        return f"{self.parent_requirement.name}:{self.name} - Category: {self.category}"


def load_requirements(file):
    requirements = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip header
        next(reader, None)
        for row in reader:
            requirements.append(Requirement(row[REQ_NAME_IDX], int(row[REQ_UNIT_TOTAL_IDX]),
                                            int(row[REQ_UNIT_LIMIT_IDX]), row[REQ_CREDIT_IDX:]))

    return requirements


def load_subrequirements(file, parent_requirements):
    subrequirements = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip header
        next(reader, None)
        for row in reader:

            # Find the parent Requirement whose name matches the one read from the file.
            parent_name = row[SUBREQ_PARENT_IDX]
            parent = None
            for req in parent_requirements:
                if parent_name == req.name:
                    parent = req

            subrequirements.append(SubRequirement(row[SUBREQ_NAME_IDX], int(row[SUBREQ_UNIT_TOTAL_IDX]),
                                                  int(row[SUBREQ_UNIT_LIMIT_IDX]), row[SUBREQ_CREDIT_IDX:],
                                                  parent))

    return subrequirements


def load_warren_subrequirements(file, parent_requirements):
    subreqs = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip header
        next(reader, None)
        for row in reader:

            # Find the parent Requirement whose name matches the read from the file.
            parent_name = row[WARR_SUBREQ_PARENT_IDX]
            parent = None
            for req in parent_requirements:
                if parent_name == req.name:
                    parent = req

            warr = WarrenSubRequirement(row[WARR_SUBREQ_NAME_IDX], int(row[WARR_SUBREQ_UNIT_TOTAL_IDX]),
                                        int(row[WARR_SUBREQ_UNIT_LIMIT_IDX]), row[WARR_SUBREQ_CREDIT_IDX:],
                                        parent, row[WARR_SUBREQ_CATEGORY_IDX])
            subreqs.append(warr)
    return subreqs