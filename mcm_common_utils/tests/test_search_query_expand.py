import pytest
import structlog

from mcm_common_utils.nlp.search_query_expand import recombine, flatten, expand_search

logger = structlog.getLogger()


def test_recombine_single_list():
    word_lists = [["color", "colors"]]
    expected_output = ["color", "colors"]
    assert recombine(word_lists) == expected_output


def test_recombine_multiple_lists():
    word_lists = [["color", "colors"], ["match", "matches"]]
    expected_output = [
        "color match", "color matches",
        "colors match", "colors matches"
    ]
    assert recombine(word_lists) == expected_output


def test_recombine_empty_list():
    word_lists = []
    expected_output = []
    assert recombine(word_lists) == expected_output


def test_recombine_single_word_lists():
    word_lists = [["color"], ["match"]]
    expected_output = ["color match"]
    assert recombine(word_lists) == expected_output


def test_flatten_single_list():
    list_of_lists = [["color", "colors"]]
    expected_output = ["color", "colors"]
    assert sorted(flatten(list_of_lists)) == sorted(expected_output)


def test_flatten_multiple_lists():
    list_of_lists = [["color", "colors"], ["match", "matches"]]
    expected_output = ["color", "colors", "match", "matches"]
    assert sorted(flatten(list_of_lists)) == sorted(expected_output)


def test_flatten_empty_list():
    list_of_lists = []
    expected_output = []
    assert flatten(list_of_lists) == expected_output


def test_flatten_with_duplicates():
    list_of_lists = [["color", "colors"], ["color", "matches"]]
    expected_output = ["color", "colors", "matches"]
    assert sorted(flatten(list_of_lists)) == sorted(expected_output)


def test_expand_search_single_word_1():
    input_phrase = "color"
    expected_output = [
        "color", "colors", "colour", "colours"
    ]
    actual_output = expand_search(input_phrase)
    logger.debug(f"expected_output: {expected_output}")
    logger.debug(f"actual_output: {actual_output}")
    assert sorted(set(expected_output)) == sorted(set(actual_output))


def test_expand_search_single_word_2():
    input_phrase = "walk"
    expected_output = [
        "walk", "walked", "walking", "walks"
    ]
    actual_output = expand_search(input_phrase)
    logger.debug(f"expected_output: {expected_output}")
    logger.debug(f"actual_output: {actual_output}")
    assert sorted(set(expected_output)) == sorted(set(actual_output))


def test_expand_search_single_word_3():
    input_phrase = "eat"
    expected_output = [
        "eat", "ate", "eaten", "eating", "eats"
    ]
    actual_output = expand_search(input_phrase)
    logger.debug(f"expected_output: {expected_output}")
    logger.debug(f"actual_output: {actual_output}")
    assert sorted(set(expected_output)) == sorted(set(actual_output))


def test_expand_search_phrase_1():
    input_phrase = "electric car"
    expected_output = [
        "electric car", "electric cars", "electrics car", "electrics cars"
    ]
    actual_output = expand_search(input_phrase)
    logger.debug(f"expected_output: {expected_output}")
    logger.debug(f"actual_output: {actual_output}")
    assert sorted(expand_search(input_phrase)) == sorted(expected_output)


def test_expand_search_phrase_2():
    input_phrase = "electrical car"
    expected_output = [
        "electrical car", "electrical cars", "electricals car", "electricals cars"
    ]
    actual_output = expand_search(input_phrase)
    logger.debug(f"expected_output: {expected_output}")
    logger.debug(f"actual_output: {actual_output}")
    assert sorted(expand_search(input_phrase)) == sorted(expected_output)


def test_expand_search_phrase_3():
    input_phrase = "breast cancer"
    expected_output = [
        "breast cancer", "breasts cancer", "breast cancers", "breasts cancers"
    ]
    actual_output = expand_search(input_phrase)
    logger.debug(f"expected_output: {expected_output}")
    logger.debug(f"actual_output: {actual_output}")
    assert sorted(expand_search(input_phrase)) == sorted(expected_output)


def test_expand_search_phrase_4():
    input_phrase = "small breast cancer"
    expected_output = [
        "breast cancer", "breasts cancer", "breast cancers", "breasts cancers"
    ]
    actual_output = expand_search(input_phrase)
    logger.debug(f"expected_output: {expected_output}")
    logger.debug(f"actual_output: {actual_output}")
    assert sorted(expand_search(input_phrase)) == sorted(expected_output)


def test_expand_search_empty_string():
    input_phrase = ""
    expected_output = [""]
    assert expand_search(input_phrase) == expected_output


# def test_expand_search_single_word_with_synonyms():
#     input_phrase = "happy"
#     expected_output = [
#         "happy", "happier", "happiest", "content", "contented", "joyful", "joyous"
#     ]
#     assert sorted(expand_search(input_phrase)) == sorted(expected_output)
#
#
# def test_expand_search_phrase_with_synonyms():
#     input_phrase = "fast car"
#     expected_output = [
#         "fast car", "fast cars", "quick car", "quick cars", "rapid car", "rapid cars"
#     ]
#     assert sorted(expand_search(input_phrase)) == sorted(expected_output)


if __name__ == '__main__':
    pytest.main()
