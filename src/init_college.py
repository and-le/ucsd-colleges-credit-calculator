import csv

from src.requirements import Requirement, SubRequirement, WarrenSubRequirement
from .requirement_constants import *
from .revelle import RevelleCollege
from .muir import MuirCollege
from .marshall import MarshallCollege
from .warren import WarrenCollege
from .roosevelt import RooseveltCollege
from .sixth import SixthCollege
from .seventh import SeventhCollege

# College names
REVELLE_NAME = "Revelle"
MUIR_NAME = "Muir"
MARSHALL_NAME = "Marshall"
WARREN_NAME = "Warren"
ROOSEVELT_NAME = "Roosevelt"
SIXTH_NAME = "Sixth"
SEVENTH_NAME = "Seventh"

# Paths to college requirement files
REVELLE_REQ_FILE = "../requirement_files/revelle-requirements.csv"
MUIR_REQ_FILE = "../requirement_files/muir-requirements.csv"
MUIR_SUBREQ_FILE = "../requirement_files/muir-subrequirements.csv"
MARSHALL_REQ_FILE = "../requirement_files/marshall-requirements.csv"
WARREN_REQ_FILE = "../requirement_files/warren-requirements.csv"
WARREN_POFC_FILE = "../requirement_files/warren-programs-of-concentration.csv"
WARREN_AS_FILE = "../requirement_files/warren-area-studies.csv"
ROOSEVELT_REQ_FILE = "../requirement_files/roosevelt-requirements.csv"
SIXTH_REQ_FILE = "../requirement_files/sixth-requirements.csv"
SEVENTH_REQ_FILE = "../requirement_files/seventh-requirements.csv"

# Names of certain requirements
MUIR_SOC_REQ_NAME = "Social Sciences"
MUIR_POLI_SUBREQ_NAME = "Political Science"
MUIR_SCI_REQ_NAME = "Math or Natural Sciences"
MUIR_CHEM_SUBREQ_NAME = "Chemistry"

WARREN_HUM_AS_NAME = "Humanities"
WARREN_SOC_AS_NAME = "Perspectives of Social Science"
WARREN_MUS_AS_NAME = "Music"
WARREN_PSY_AS_NAME = "Psychology"

def init_college(name):
    """
    Convenience method for instantiating a college.
    :param name: name of the college to instantiate
    :return: a created college
    """

    college = None

    if name == REVELLE_NAME:
        reqs = load_requirements(REVELLE_REQ_FILE)
        college = RevelleCollege(REVELLE_NAME, reqs)
    elif name == MUIR_NAME:
        reqs = load_requirements(MUIR_REQ_FILE)
        subreqs = load_subrequirements(MUIR_SUBREQ_FILE, reqs)
        college = MuirCollege(MUIR_NAME, reqs, subreqs)
    elif name == MARSHALL_NAME:
        reqs = load_requirements(MARSHALL_REQ_FILE)
        college = MarshallCollege(MARSHALL_NAME, reqs)
    elif name == WARREN_NAME:
        reqs = load_requirements(WARREN_REQ_FILE)
        pofc = load_warren_subrequirements(WARREN_POFC_FILE, reqs)
        area = load_warren_subrequirements(WARREN_AS_FILE, reqs)
        college = WarrenCollege(WARREN_NAME, reqs, pofc, area)
    elif name == ROOSEVELT_NAME:
        reqs = load_requirements(ROOSEVELT_REQ_FILE)
        college = RooseveltCollege(ROOSEVELT_NAME, reqs)
    elif name == SIXTH_NAME:
        reqs = load_requirements(SIXTH_REQ_FILE)
        college = SixthCollege(SIXTH_NAME, reqs)
    elif name == SEVENTH_NAME:
        reqs = load_requirements(SEVENTH_REQ_FILE)
        college = SeventhCollege(SEVENTH_NAME, reqs)

    return college


def load_requirements(file):
    """
    Returns a List of Requirements from the read file.
    :param file: CSV file to load the requirements for a college from
    :return: a List of Requirement objects
    """
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
    """
    Returns a List of SubRequirements from the read file. The parameter
    parent_requirements must be obtained by calling the load_requirements() method first
    :param file: CSV file to load the requirements for a college from
    :param parent_requirements: List of Requirement objects
    :return: a List of Requirement objects
    :return: a List of SubRequirements
    """
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
    """
    Returns a List of WarrenSubRequirements from the read file. The parameter
    parent_requirements must be obtained by calling the load_requirements() method first.
    This method is different from load_subrequirements() in that the CSV files for Warren College
    are indexed differently than the Muir College CSV files.
    :param file: CSV file to load the requirements for a college from
    :param parent_requirements: List of Requirement objects
    :return: a List of Requirement objects
    :return: a List of WarrenSubRequirements
    """
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