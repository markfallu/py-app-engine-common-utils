import pytest
import spacy

from ..nlp.synonyms import get_synonyms, get_lemmatized_variants, RETURN_TYPE_STRING, RETURN_TYPE_LIST

# Load spaCy model
nlp = spacy.load('en_core_web_sm')


def test_get_synonyms_single_word():
    term_list = ['happy']
    expected_output = '["felicitous","glad","happy","well-chosen"]'  # Example expected output
    assert get_synonyms(term_list, RETURN_TYPE_STRING) == expected_output


def test_get_synonyms_multi_word():
    term_list = ['cow milk']
    expected_output = '["cow milk","cow milk river","moo-cow milk","moo-cow milk river"]'  # Example expected output
    assert get_synonyms(term_list, RETURN_TYPE_STRING) == expected_output


def test_get_synonyms_return_list():
    term_list = ['happy']
    expected_output = ['felicitous', 'glad', 'happy', 'well-chosen']  # Example expected output
    assert get_synonyms(term_list, RETURN_TYPE_LIST) == expected_output


def test_get_synonyms_empty_list():
    term_list = []
    expected_output = None
    assert get_synonyms(term_list, RETURN_TYPE_STRING) == expected_output


def test_get_synonyms_no_synonyms():
    term_list = ['qwerty']
    expected_output = '["qwerty"]'  # Example expected output
    assert get_synonyms(term_list, RETURN_TYPE_STRING) == expected_output


def test_get_lemmatized_variants_single_word():
    text = "running"
    expected_output = ["running", "run"]
    assert get_lemmatized_variants(text) == expected_output


def test_get_lemmatized_variants_sentence():
    text = "The cats are running"
    expected_output = ["The cats are running", "the cat be run"]
    assert get_lemmatized_variants(text) == expected_output


def test_get_lemmatized_variants_empty_string():
    text = ""
    expected_output = []
    assert get_lemmatized_variants(text) == expected_output


def test_get_lemmatized_variants_punctuation():
    text = "Hello, world!"
    expected_output = ["Hello, world!", "hello , world !"]
    assert get_lemmatized_variants(text) == expected_output


def test_get_lemmatized_variants_mixed_case():
    text = "Running FAST"
    expected_output = ["Running FAST", "run FAST"]
    assert get_lemmatized_variants(text) == expected_output


if __name__ == '__main__':
    pytest.main()
