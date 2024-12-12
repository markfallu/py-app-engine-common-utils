import re
import sys

import spacy
from nltk.corpus import cmudict
from nltk.corpus import wordnet

from .constants import CHAR_SPACE, RETURN_TYPE_STRING, RETURN_TYPE_LIST
from .pluralize import get_singular_and_plurals as plural
from .termset_expander import get_verb_base_form, unique_inflections, expand
from .verb_inflector import get_inflections

# Need to import 'util.py', which lives in the nlp directory two levels up.
# This is a hack, and we really need a better solution...
module_dir = sys.path[0]
pos = module_dir.find('/nlp')
if -1 != pos:
    # get path to nlp directory and append to sys.path
    nlp_dir = module_dir[:pos + 4]
    sys.path.append(nlp_dir)
# import util

# load Spacy's English model
nlp = spacy.load('en_core_web_sm')

# initialize the CMU phoneme dictionary
cmu_dict = cmudict.dict()


###############################################################################
def get_single_word_synonyms(word, pos):
    """
    Return a list of synonyms for the given word with part of speech 'pos'.
    """

    assert pos == wordnet.NOUN or pos == wordnet.ADJ or pos == wordnet.ADV

    synonyms = []

    # get all sets of synonyms from Wordnet
    synsets = wordnet.synsets(word.lower(), pos)
    for s in synsets:
        # the 'lemmas' for each set are the synonyms
        synonyms.extend(s.lemma_names())

    if len(synonyms) > 0:
        synonyms = [s.lower() for s in synonyms]
        uniques = sorted(list(set(synonyms)))
    else:
        uniques = [word]

    # rearrange so that the given word comes first
    if len(uniques) > 1:
        swap_index = uniques.index(word)
        uniques[0], uniques[swap_index] = uniques[swap_index], uniques[0]

    return uniques


###############################################################################
def to_string(term_list, suffix=''):
    """
    Convert a list of terms to a single string representing the result of
    macro expansion.
    """

    if 0 == len(term_list):
        return None

    terms = ['"' + t + suffix + '"' for t in term_list]
    term_string = ','.join(terms)

    # enclose in brackets to represent an array
    term_string = '[' + term_string + ']'
    return term_string


###############################################################################
def get_synonyms(term_list, return_type=RETURN_TYPE_STRING):
    synonyms = []
    for t in term_list:

        # if t contains a space, assume multiword term
        is_multiword = -1 != t.find(CHAR_SPACE)

        # get synonyms for term as a whole, whether multiword or not
        pos = [wordnet.NOUN, wordnet.ADJ, wordnet.ADV]
        for p in pos:
            new_syns = get_single_word_synonyms(word=t, pos=p)
            synonyms.extend(new_syns)

        # include the term itself if not already present
        if t not in synonyms:
            synonyms.append(t)

        if is_multiword:
            # get parts of speech
            doc = nlp(t)
            if 1 == len(doc):
                continue

            # multi-word
            index_map = {}
            for token in doc:
                if 'NOUN' == token.pos_:
                    index_map[token.i] = (token.text, wordnet.NOUN)
                elif 'ADJ' == token.pos_:
                    index_map[token.i] = (token.text, wordnet.ADJ)
                elif 'ADV' == token.pos_:
                    index_map[token.i] = (token.text, wordnet.ADV)

            # if no entries, nothing to do
            if not index_map:
                continue
            else:
                # split into individual words
                words = t.split()

                # update indices in case spacy did not fully tokenize
                ok = True
                for index, token_and_pos in index_map.items():
                    if index < len(words):
                        token = token_and_pos[0]
                        if words[index] == token:
                            continue

                    # spacy tokenization is different from t.split()
                    for j in len(words):
                        if words[j] == token:
                            del index_map[index]
                            index_map[j] = token_and_pos
                        else:
                            # not found
                            ok = False
                            break

                    if not ok:
                        # treat this term t as being a single word
                        break

                if not ok:
                    continue

            # rebuild the index map with all synonyms
            for index, token_and_pos in index_map.items():
                token = token_and_pos[0]
                pos = token_and_pos[1]
                syns = get_single_word_synonyms(word=token, pos=pos)
                index_map[index] = syns

            # do the expansion
            #log('index map: {0}'.format(index_map))
            new_phrases = expand(t, index_map)
            #log('new phrases: {0}'.format(new_phrases))
            synonyms.extend(new_phrases)

    # convert to lowercase, remove duplicates, and sort
    if len(synonyms) > 0:
        synonyms = [s.lower() for s in synonyms]
        term_list = sorted(list(set(synonyms)))

    # remove WordNet underscores
    term_list = [re.sub(r'_', ' ', t) for t in term_list]

    if RETURN_TYPE_LIST == return_type:
        return term_list
    else:
        return to_string(term_list)


###############################################################################
def get_single_verb_inflections(term):
    """
    Get all inflections for the given term.
    """

    verb = term.lower()
    base_form = get_verb_base_form(verb)
    inflections = get_inflections(base_form)
    # remove duplicates in the inflections
    verbs = unique_inflections(inflections)
    return verbs


###############################################################################
def get_verb_inflections(namespace, term_list, return_type=RETURN_TYPE_STRING):
    new_terms = []
    for t in term_list:

        # if t contains a space, assume multiword term
        is_multiword = -1 != t.find(CHAR_SPACE)

        # assume verb if single word
        if not is_multiword:
            verbs = get_single_verb_inflections(t)
            new_terms.extend(verbs)
        else:
            # get parts of speech and find verbs
            doc = nlp(t)
            if 1 == len(doc):
                verbs = get_single_verb_inflections(t)
                new_terms.extend(verbs)
                continue

            # multi-word
            index_map = {}
            for token in doc:
                if 'VERB' == token.pos_:
                    index_map[token.i] = token.text

            # if no verbs, no inflections to compute
            if not index_map:
                verbs = get_single_verb_inflections(t)
                new_terms.extend(verbs)
                continue
            else:
                # split into individual words
                words = t.split()

                # update indices in case spacy did not fully tokenize
                ok = True
                for index, token in index_map.items():
                    if index < len(words):
                        token = index_map[index]
                        if words[index] == token:
                            continue

                    # spacy tokenization is different from t.split()
                    for j in len(words):
                        if words[j] == token:
                            del index_map[index]
                            index_map[j] = token
                        else:
                            # not found
                            ok = False
                            break

                    if not ok:
                        # treat as single word
                        verbs = get_single_verb_inflections(t)
                        new_terms.extend(verbs)
                        break

                if not ok:
                    continue

            # rebuild the index map with all inflections
            for index, token in index_map.items():
                verbs = get_single_verb_inflections(token)
                index_map[index] = verbs

            # do the expansion
            new_phrases = expand(t, index_map)
            new_terms.extend(new_phrases)

    # remove duplicates
    if len(new_terms) > 0:
        term_list = sorted(list(set(new_terms)))

    if RETURN_TYPE_LIST == return_type:
        return term_list
    else:
        return to_string(term_list)


###############################################################################
def get_plurals(namespace, term_list, return_type=RETURN_TYPE_STRING):
    new_terms = []
    for t in term_list:
        # include the original term also
        new_terms.append(t)
        plural_terms = plural(t.lower())
        new_terms.extend(plural_terms)
    term_list = new_terms

    if RETURN_TYPE_LIST == return_type:
        return term_list
    else:
        return to_string(term_list)


###############################################################################
def get_lexical_variants(namespace, term_list):
    inflected_terms = get_verb_inflections(namespace, term_list, RETURN_TYPE_LIST)
    new_terms = get_plurals(namespace, inflected_terms, RETURN_TYPE_LIST)

    # remove duplicates and sort
    if len(new_terms) > 0:
        term_list = sorted(list(set(new_terms)))

    return to_string(term_list)


###############################################################################
def get_pronunciations(word):
    """
    Return the list of pronunciations for the given word, if any.
    """

    phoneme_lists = []
    try:
        phoneme_lists = cmu_dict[word]
    except:
        pass

    return phoneme_lists


###############################################################################
def get_lemmatized_variants(text):
    if text == '':
        return []
    term_list = [text]

    # Process the text using spaCy
    doc = nlp(text)

    # Extract lemmatized tokens
    lemmatized_tokens = [token.lemma_ for token in doc]

    # Join the lemmatized tokens into a sentence
    lemmatized_text = ' '.join(lemmatized_tokens)

    # Append the lemmatized text
    term_list.append(lemmatized_text)

    return term_list

###############################################################################
