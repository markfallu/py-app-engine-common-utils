# tests/test_pluralize.py

import pytest
from ..nlp.pluralize import get_singular_and_plurals as plural


def test_plural_single_word():
    assert plural('cat') == ['cat', 'cats']


def test_plural_phrase():
    assert plural('dog house') == ['dog house', 'dog houses']


def test_plural_irregular():
    assert plural('child') == ['child', 'children']


def test_plural_empty_string():
    assert plural('') == ['']


def test_singular_single_word():
    assert plural('cats') == ['cats', 'cat']


def test_singular_phrase():
    assert plural('dog houses') == ['dog houses', 'dog house']


def test_singular_irregular():
    assert plural('children') == ['children', 'child']


if __name__ == '__main__':
    pytest.main()
