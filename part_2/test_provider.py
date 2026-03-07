import unittest
from datetime import date
from decimal import Decimal

from lab_2_part_2 import Provider


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
        self.invoice_15kg_2x_4lines = InvoiceStub(
            number="INV-001",
            currency="EUR",
            kilos=Decimal(15.0),
            unit=Decimal(2.0),
            total=Decimal(4.0),
        )

        self.invoice_22kg_3x_1line = InvoiceStub(
            number="INV-002",
            currency="JPY",
            kilos=Decimal(22.0),
            unit=Decimal(3.0),
            total=Decimal(1.0),
        )

        self.invoice_0kg_1x_1line = InvoiceStub(
            number="INV-003",
            currency="USD",
            kilos=Decimal(0.0),
            unit=Decimal(1.0),
            total=Decimal(1.0),
        )

        self.invoice_1kg_0x_1line = InvoiceStub(
            number="INV-004",
            currency="GBP",
            kilos=Decimal(1.0),
            unit=Decimal(0.0),
            total=Decimal(1.0),
        )

    def test_add_bill(self) -> None:
        self.provider.add_bill(self.invoice_15kg_2x_4lines)
        self.assertIn(self.invoice_15kg_2x_4lines, self.provider.bills)

    def test_add_another_bill(self) -> None:
        self.provider.add_bill(self.invoice_15kg_2x_4lines)
        self.assertIn(self.invoice_15kg_2x_4lines, self.provider.bills)

        self.provider.add_bill(self.invoice_22kg_3x_1line)
        self.assertIn(self.invoice_15kg_2x_4lines, self.provider.bills)

        self.assertEqual(len(self.provider.bills), 2)

    def test_no_kilos_to_bill(self) -> None:
        total = self.provider.total_kilos_to_bill()
        self.assertEqual(total, 0)

    def test_total_kilos_to_bill(self) -> None:
        self.provider.add_bill(self.invoice_15kg_2x_4lines)

        total = self.provider.total_kilos_to_bill()
        self.assertEqual(total, 15)

    def test_avg_unit_price_zero(self) -> None:
        avg = self.provider.avg_unit_price()
        self.assertEqual(avg, 0)

        self.provider.add_bill(self.invoice_0kg_1x_1line)

        avg = self.provider.avg_unit_price()
        self.assertEqual(avg, 0)

        self.provider.add_bill(self.invoice_1kg_0x_1line)

        avg = self.provider.avg_unit_price()
        self.assertEqual(avg, 0)

    def test_avg_unit_price(self) -> None:
        self.provider.add_bill(self.invoice_15kg_2x_4lines)

        avg = self.provider.avg_unit_price()
        self.assertEqual(avg, 2)

        self.provider.add_bill(self.invoice_22kg_3x_1line)

        avg = self.provider.avg_unit_price()
        self.assertAlmostEqual(avg, Decimal(2.594594594))

    def test_invoice_amount_no_invoice(self) -> None:
        total = self.provider.total_invoice_amount()
        self.assertEqual(total, 0)

    def test_invoice_amount(self) -> None:
        self.provider.add_bill(self.invoice_15kg_2x_4lines)

        total = self.provider.total_invoice_amount()
        self.assertEqual(total, 4)

        self.provider.add_bill(self.invoice_22kg_3x_1line)

        total = self.provider.total_invoice_amount()
        self.assertEqual(total, 5)
