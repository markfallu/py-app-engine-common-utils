import inflect
import spacy
import structlog
from nltk import flatten

from .constants import EMPTY_STRING
from .verb_inflector import get_inflections

logger = structlog.getLogger()
nlp = spacy.load("en_core_web_sm")
engine = inflect.engine()


# Define a function to check if a word is a verb
def is_verb(word):
    doc = nlp(word)
    return any(token.pos_ == "VERB" for token in doc)


def get_singular_and_plurals(text):
    """
    The input text is either a single word or a phrase, assumed SINGULAR.

    This function determines the plural forms of the input text and returns
    a list of those forms. Both modern and 'classical' plurals are returned.
    """

    if text == EMPTY_STRING:
        return [EMPTY_STRING]

    result_list = [text]

    if is_plural(text):
        singular = engine.singular_noun(text)
        if singular not in result_list:
            result_list.append(singular)
        return result_list

    modern_plural = engine.plural(text)
    result_list.append(modern_plural)

    engine.classical()
    classical_plural = engine.plural(text)
    if classical_plural not in result_list:
        result_list.append(classical_plural)
    engine.classical(all=False)

    if is_verb(text):
        verb_inflections = get_inflections(text)
        logger.debug(f"Verb inflections for {text} are: {flatten(verb_inflections)}")
        for term in flatten(verb_inflections):
            if term not in result_list:
                result_list.append(term)
    return result_list


def is_plural(word):
    # Check if the word is plural
    return engine.singular_noun(word) is not False


def get_singular_if_plural(word):
    # Get the singular form if the word is plural
    singular = engine.singular_noun(word)
    return singular if singular else word


def plural(text):
    """
    The input text is either a single word or a phrase, assumed SINGULAR.

    This function determines the plural forms of the input text and returns
    a list of those forms. Both modern and 'classical' plurals are returned.
    """

    result_list = []

    modern_plural = engine.plural(text)
    result_list.append(modern_plural)

    engine.classical()
    classical_plural = engine.plural(text)
    if classical_plural not in result_list:
        result_list.append(classical_plural)
    engine.classical(all=False)

    return result_list
