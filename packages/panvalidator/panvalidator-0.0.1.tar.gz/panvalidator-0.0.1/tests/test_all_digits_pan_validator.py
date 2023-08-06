from panvalidator import AllDigitsPanValidator


def test_pan_contains_only_digits():
    validator = AllDigitsPanValidator()
    result = validator.validate('1234567890')
    assert result.is_valid()
    assert result.message == ''


def test_pan_contains_other_symbols():
    validator = AllDigitsPanValidator()
    result = validator.validate('a1b2c3')
    assert not result.is_valid()
    assert result.message == 'PAN should have only digits, found: a, b, c.'
