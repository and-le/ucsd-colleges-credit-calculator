VALID_EXAM_SCORES = [1, 2, 3, 4, 5]

def is_valid_exam_score(score):
    """
    Returns True if the given string represents a valid AP Exam score; False otherwise
    :param score:
    :return:
    """
    try:
        score_as_int = int(score)
        # If the score is an integer, check that it is one of the valid scores
        return score_as_int in VALID_EXAM_SCORES
    except:
        return False


