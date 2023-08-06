from panvalidator import LengthPanValidator


def test_valid_pan_length():
    validator = LengthPanValidator()
    result = validator.validate('1234567812345678')
    assert result.is_valid()
    assert result.message == ''


def test_invalid_pan_length():
    validator = LengthPanValidator()
    result = validator.validate('1111')
    assert not result.is_valid()
    assert result.message == 'Invalid length 4.'
