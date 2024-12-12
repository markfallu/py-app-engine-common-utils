import pytest
import structlog

from ..nlp.constants import EMPTY_STRING
from ..nlp.spelling import get_spelling_variants

logger = structlog.getLogger()


def test_get_spelling_variants_empty_string(mocker):
    assert get_spelling_variants(EMPTY_STRING) == EMPTY_STRING


def test_get_spelling_variants_american_spelling(mocker):
    mocker.patch('breame.spelling.american_spelling_exists', return_value=True)
    mocker.patch('breame.spelling.get_british_spelling', return_value='colour')
    assert get_spelling_variants('color') == ['color', 'colour']


def test_get_spelling_variants_british_spelling(mocker):
    mocker.patch('breame.spelling.american_spelling_exists', return_value=False)
    mocker.patch('breame.spelling.british_spelling_exists', return_value=True)
    mocker.patch('breame.spelling.get_american_spelling', return_value='color')
    assert get_spelling_variants('colour') == ['colour', 'color']


def test_get_spelling_variants_no_spelling_variant(mocker):
    mocker.patch('breame.spelling.american_spelling_exists', return_value=False)
    mocker.patch('breame.spelling.british_spelling_exists', return_value=False)
    assert get_spelling_variants('test') == ['test']


def test_get_spelling_variants_american_spelling_2(mocker):
    mocker.patch('breame.spelling.american_spelling_exists', return_value=True)
    mocker.patch('breame.spelling.get_british_spelling', return_value='vaporize')
    assert get_spelling_variants('vaporize') == ['vaporize', 'vaporise']


def test_get_spelling_variants_british_spelling_2(mocker):
    mocker.patch('breame.spelling.american_spelling_exists', return_value=False)
    mocker.patch('breame.spelling.british_spelling_exists', return_value=True)
    mocker.patch('breame.spelling.get_american_spelling', return_value='vaporise')
    assert get_spelling_variants('vaporise') == ['vaporise', 'vaporize']


if __name__ == '__main__':
    pytest.main()
