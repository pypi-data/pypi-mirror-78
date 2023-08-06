from panvalidator import LuhnPanValidator, LuhnChecker


class FakeLuhnChecker(LuhnChecker):

    def __init__(self, always_valid=True):
        self._always_valid = always_valid

    def check(self, pan: str) -> bool:
        return self._always_valid


def test_valid_luhn():
    validator = LuhnPanValidator(FakeLuhnChecker())
    result = validator.validate('11111')
    assert result.is_valid()
    assert result.message == ''


def test_invalid_luhn():
    validator = LuhnPanValidator(FakeLuhnChecker(always_valid=False))
    result = validator.validate('11111')
    assert not result.is_valid()
    assert result.message == 'Invalid luhn.'
