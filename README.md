# ucsd-colleges-credit-calculator

# Overview
A web-based application to help high school seniors 
determine how much AP Credit will be accepted at each 
UC San Diego undergraduate college.

This application uses the official undergraduate requirements found at
https://www.ucsd.edu/catalog/pdf/APC-chart.pdf to determine how many credits
each AP Couse counts for at each UC San Diego college. College-specific
requirements can be found at each undergraduate college's general education
requirement page, which can be accessed at https://admissions.ucsd.edu/why/colleges/
. 

# Adding a New College
To add a new college so the AP credit calculation can be used for the college, follow these steps:

1. Create a new college class that subclasses the base `College` class from `college.py`.
2. Implement the `apply_credits` method for the class.
3. In the `init_college.py` file, define a name variable for the new college and add it to the `COLLEGE_NAMES` list.
4. In `src/requirement_files`, add a CSV file for the requirements for that college.
5. In the `init_college` method in `init_college.py`, add code to load the requirements for the new college.

# Terminology

## "Requirement" versus "Course"
1. A "course" typically corresponds to an individual AP course. 
2. A "requirement" is a policy specified by a college indicating one or more courses that must be completed for the requirement itself to be completed.

# Notes
**This application is based on the requirements for the 2019 - 2020 academic year. Since then, there have been the following important changes:**

1. New colleges have been introduced.
2. Course requirements and eligible AP credit has changed.


