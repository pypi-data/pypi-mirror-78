from difflib import ndiff
import panvalidator


def test_valid_pan():
    result = panvalidator.validate('4444444444444422')
    assert result.is_valid(), result.message
    assert result.message == ''


def test_invalid_length():
    result = panvalidator.validate('44')
    assert not result.is_valid(), result.message
    expected = """Given PAN has following issue(s):
  1. Invalid length 2.
  2. Invalid IIN 44.
  3. Invalid luhn."""
    assert_message(expected, result.message)


def test_has_symbols():
    result = panvalidator.validate('ab')
    assert not result.is_valid(), result.message
    expected = """Given PAN has following issue(s):
  1. Invalid length 2.
  2. PAN should have only digits, found: a, b.
  3. Invalid IIN -1.
  4. Invalid luhn."""
    assert_message(expected, result.message)


def test_invalid_iin():
    result = panvalidator.validate('3569380356438096')
    assert not result.is_valid(), result.message
    expected = """Given PAN has following issue(s):
  1. Invalid IIN 3569."""
    assert_message(expected, result.message)


def test_empty_pan():
    result = panvalidator.validate('')
    assert not result.is_valid(), result.message
    expected = """Given PAN has following issue(s):
  1. Invalid length 0.
  2. Invalid IIN -1."""
    assert_message(expected, result.message)


def assert_message(expected, actual):
    assert actual == expected, ''.join(
        ndiff(actual.splitlines(keepends=True),
              expected.splitlines(keepends=True)))
