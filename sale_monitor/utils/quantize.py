from decimal import Decimal
from typing import Union


def quantize(value: Union[int, float, str]) -> Decimal:
    # Enforces 2 decimal places
    return Decimal(value).quantize(Decimal('1.00'))

