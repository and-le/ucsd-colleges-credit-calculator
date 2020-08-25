from src.ap_constants import  *
from src.requirements import *
from src.init_college import  *
if __name__ == "__main__":
    credits = [
        APCredit(AP_CALC_AB, 3),
        APCredit(AP_CALC_BC, 5),
    ]
    college = init_college(SIXTH_NAME)
    college.apply_credits(credits)
    print(college.credited_units)
