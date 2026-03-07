import unittest
from datetime import date
from decimal import Decimal
from typing import List

from lab_2_part_2 import InvoiceLine, Provider


class InvoiceStub:
    def __init__(
        self,
        number: str,
        currency: str,
        kilos: Decimal,
        unit: Decimal,
        total: Decimal,
        date: date = date.today(),
    ) -> None:
        self.number = number
        self.date = date
        self.currency = currency
        self.kilos = kilos
        self.unit = unit
        self._total = total

    def kilos_to_bill(self) -> Decimal:
        return self.kilos

    def unit_price(self) -> Decimal:
        return self.unit

    @property
    def total(self) -> Decimal:
        return self._total


class TestProvider(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = Provider(name="ACME")
        self.invoice_ = InvoiceStub(
            number="INV-001",
            currency="EUR",
            kilos=Decimal(15.0),
            unit=Decimal(2.0),
            total=Decimal(4.0),
        )
