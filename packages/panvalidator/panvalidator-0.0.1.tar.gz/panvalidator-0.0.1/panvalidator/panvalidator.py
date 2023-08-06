"""Panvalidator tool."""
from typing import List
import luhn


class ValidationResult:
    """Result of PAN validation."""

    def __init__(self, valid: bool, message: str = ""):
        self._valid = valid
        self._message = message

    def is_valid(self) -> bool:
        """If result is valid."""
        return self._valid

    @property
    def message(self) -> str:
        """Result message."""
        return self._message

    @classmethod
    def valid(cls):
        """Construct valid |ValidationResult|."""
        return cls(valid=True, message='')

    @classmethod
    def invalid(cls, message):
        """Construct invalid |ValidationResult|."""
        return cls(valid=False, message=message)


def validate(pan: str) -> ValidationResult:
    """Validate PAN using multiple validators."""
    return CompositePanValidator.default().validate(pan)


class PanValidator:
    """Base validator for PAN validation."""

    def validate(self, pan: str) -> ValidationResult:
        """Perform PAN validation and return |ValidationResult|."""
        raise NotImplementedError()


PAN_LENGTH = 16


class LengthPanValidator(PanValidator):
    """Validator to validate PAN length."""

    def validate(self, pan: str) -> ValidationResult:
        pan_length = len(pan)
        is_valid = pan_length == PAN_LENGTH

        if not is_valid:
            message = f'Invalid length {pan_length}.'
            return ValidationResult.invalid(message=message)

        return ValidationResult.valid()


class AllDigitsPanValidator(PanValidator):
    """Validator to validate PAN has only digits."""

    def validate(self, pan: str) -> ValidationResult:
        is_valid = all(it.isdigit() for it in pan)

        if not is_valid:
            non_digits = ', '.join(
                list(filter(lambda x: not x.isdigit(), pan)))
            message = f'PAN should have only digits, found: {non_digits}.'
            return ValidationResult.invalid(message=message)

        return ValidationResult.valid()


class PaymentSystem:
    """A payment system with issuer identification number.
    See https://en.wikipedia.org/wiki/Payment_card_number."""

    def __init__(self, *ranges):
        self._ranges = ranges

    @property
    def iin(self):
        """Range of all possible issuer identification numbers."""
        result_range = []
        for _range in self._ranges:
            result_range += list(_range)
        return result_range


MASTER_CARD = PaymentSystem(range(2221, 2721), range(5100, 5600))
VISA = PaymentSystem(range(4000, 5000))
MIR = PaymentSystem(range(2200, 2205))


SUPPORTED_PAYMENT_SYSTEMS = [
    MASTER_CARD,
    VISA,
    MIR
]


IIN_LENGTH = 4


def safe_int(to_int: str) -> int:
    """Return int from str safely."""
    try:
        return int(to_int)
    except ValueError:
        return -1


class PaymentSystemPanValidator(PanValidator):
    """Validator to validate payment system."""

    def validate(self, pan: str) -> ValidationResult:
        iin = safe_int(pan[:IIN_LENGTH])
        found = False
        for payment_system in SUPPORTED_PAYMENT_SYSTEMS:
            if iin in payment_system.iin:
                found = True
                break

        if not found:
            return ValidationResult.invalid(message=f'Invalid IIN {iin}.')

        return ValidationResult.valid()


class LuhnChecker:
    """A luhn checker."""

    def check(self, pan: str) -> bool:
        raise NotImplementedError()


class RealLuhnChecker(LuhnChecker):
    """Implementation of |LuhnChecker| that does verify luhn."""

    def check(self, pan: str) -> bool:
        try:
            return luhn.verify(pan)
        except ValueError:
            return False


class LuhnPanValidator(PanValidator):
    """Validator to validate PAN's luhn."""

    def __init__(self, checker=RealLuhnChecker()):
        self._checker = checker

    def validate(self, pan: str) -> ValidationResult:
        is_valid = self._checker.check(pan)
        if not is_valid:
            return ValidationResult.invalid(message='Invalid luhn.')

        return ValidationResult.valid()


class CompositePanValidator(PanValidator):
    """Composite PAN validator that combines different validators."""

    def __init__(self, *validators: List[PanValidator]):
        self._validators = validators

    def validate(self, pan: str) -> ValidationResult:
        messages = []
        for validator in self._validators:
            result = validator.validate(pan)
            if not result.is_valid():
                messages.append(result.message)

        if messages:
            message = CompositePanValidator._format_messages(messages)
            return ValidationResult.invalid(message=message)

        return ValidationResult.valid()

    @staticmethod
    def _format_messages(messages: List[str]) -> str:
        result = ['Given PAN has following issue(s):']
        for index, message in enumerate(messages):
            result += [f'  {index + 1}. {message}']
        return '\n'.join(result)

    @classmethod
    def default(cls):
        return cls(
            LengthPanValidator(),
            AllDigitsPanValidator(),
            PaymentSystemPanValidator(),
            LuhnPanValidator()
        )
