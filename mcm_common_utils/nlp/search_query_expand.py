from itertools import product

import structlog

from .pluralize import get_singular_and_plurals
from .spelling import get_spelling_variants
from .synonyms import get_synonyms, get_lemmatized_variants
from .tokenize import tokenize

logger = structlog.getLogger()


def expand_search(input_phrase):
    words = tokenize(input_phrase)  # Split input into individual words (up to 3 words)
    expanded_terms = []

    for word in words:
        # Step 1: Get plural and singular forms
        word_variants = set()
        singular_plurals = get_singular_and_plurals(word)
        logger.debug(f"Singular plurals for {word} are: {singular_plurals}")
        word_variants.update(singular_plurals)
        logger.debug(f"Word variants after step 1: {word_variants}")

        # Step 2: Get synonyms and their plural forms
        # synonyms = get_synonyms(word)  # Assume this returns a set of synonyms
        # logger.debug(f"Synonyms for {word} are: {synonyms}")
        # for synonym in synonyms:
        #     word_variants.update(synonym)
        #     word_variants.update(get_singular_and_plurals(synonym))

        # Step 3: Get lemmatized forms (base forms)
        lemmas = get_lemmatized_variants(word)
        logger.debug(f"Lemmas for {word} are: {lemmas}")
        for lemma in lemmas:
            singular_plurals = get_singular_and_plurals(lemma)
            word_variants.update(singular_plurals)
        logger.debug(f"Word variants after step 3: {word_variants}")

        # Step 4: Get regional spelling variations
        regional_variants = get_spelling_variants(word)
        logger.debug(f"Regional variants for {word} are: {regional_variants}")
        for regional_variant in regional_variants:
            singular_plurals = get_singular_and_plurals(regional_variant)
            word_variants.update(singular_plurals)

        logger.debug(f"Word variants after step 4: {word_variants}")

        logger.debug(f"Total word variants for {word} are: {word_variants}")
        # Add all variants of this word to the final list
        expanded_terms.append(list(word_variants))

    # Step 5: If the input was a phrase, recombine the words back into phrases
    if len(words) > 1:
        expanded_phrases = recombine(expanded_terms)  # Create all possible phrase combinations
        return expanded_phrases

    # If single word, return flattened list of expanded terms
    return flatten(expanded_terms)


def recombine(word_lists):
    if len(word_lists) == 0:
        return []
    # This function takes multiple lists of expanded words and combines them into phrases
    # Example input: [["color", "colors", "colour", "colours"], ["match", "matches"]]
    # Example output: ["color match", "colors match", "colour match", "colours match", "color matches", ...]
    return [" ".join(phrase) for phrase in product(*word_lists)]  # Cartesian product of word variants


def flatten(list_of_lists):
    # Flatten the list of expanded terms and remove duplicates
    return list(set([item for sublist in list_of_lists for item in sublist]))
