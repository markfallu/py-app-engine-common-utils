from breame.spelling import american_spelling_exists, get_british_spelling, british_spelling_exists, \
    get_american_spelling

from .constants import EMPTY_STRING


def get_spelling_variants(text):
    if text == EMPTY_STRING:
        return EMPTY_STRING

    return_list = [text]
    if american_spelling_exists(text):
        return_list.append(get_british_spelling(text))
    elif british_spelling_exists(text):
        return_list.append(get_american_spelling(text))
    return return_list
