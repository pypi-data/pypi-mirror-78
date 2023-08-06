from panvalidator import PaymentSystemPanValidator


def test_visa():
    assert_valid_iin(range(4000, 5000))


def test_mastercard():
    iins = list(range(2221, 2721)) + list(range(5100, 5600))
    assert_valid_iin(iins)


def test_mir():
    assert_valid_iin(range(2200, 2205))


def test_unsupported_iin():
    validator = PaymentSystemPanValidator()
    result = validator.validate('1111')
    assert not result.is_valid()
    assert result.message == 'Invalid IIN 1111.'


def assert_valid_iin(iins):
    validator = PaymentSystemPanValidator()
    for iin in iins:
        result = validator.validate(f'{iin}')
        assert result.is_valid(), iin
        assert result.message == ''
