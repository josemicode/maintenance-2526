import unittest
from decimal import Decimal

from lab_2_part_3 import InvoiceLine


class TestInvoiceLine(unittest.TestCase):
    def setUp(self) -> None:
        self.invoice_line_20_qty = InvoiceLine(
            seq=1,
            description="Line X",
            unitPriceEURPerKg=Decimal(2.0),
            qtyKg=Decimal(20),
        )

        self.invoice_line_zero_qty = InvoiceLine(
            seq=2,
            description="Line D",
            unitPriceEURPerKg=Decimal(7.5),
            qtyKg=Decimal(0),
        )
