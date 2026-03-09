import unittest
from decimal import Decimal
from unittest.mock import Mock, create_autospec

from lab_2_part_3 import Invoice, Provider


class TestProvider(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = Provider(name="ACME")

        self.invoice_15kg_2x_4lines = create_autospec(spec=Invoice, instance=True)
        self.invoice_15kg_2x_4lines.number = "INV-001"
        self.invoice_15kg_2x_4lines.currency = "EUR"
        self.invoice_15kg_2x_4lines.kilos = Decimal(15.0)
        self.invoice_15kg_2x_4lines.unit = Decimal(2.0)
        self.invoice_15kg_2x_4lines.kilos_to_bill.return_value = Decimal(15.0)
        self.invoice_15kg_2x_4lines.unit_price.return_value = Decimal(2.0)
        self.invoice_15kg_2x_4lines.total = Decimal(4.0)

        self.invoice_22kg_3x_1line = create_autospec(spec=Invoice, instance=True)
        self.invoice_22kg_3x_1line.number = "INV-002"
        self.invoice_22kg_3x_1line.currency = "JPY"
        self.invoice_22kg_3x_1line.kilos = Decimal(22.0)
        self.invoice_22kg_3x_1line.unit = Decimal(3.0)
        self.invoice_22kg_3x_1line.kilos_to_bill.return_value = Decimal(22.0)
        self.invoice_22kg_3x_1line.unit_price.return_value = Decimal(3.0)
        self.invoice_22kg_3x_1line.total = Decimal(1.0)

        self.invoice_0kg_1x_1line = create_autospec(spec=Invoice, instance=True)
        self.invoice_0kg_1x_1line.number = "INV-003"
        self.invoice_0kg_1x_1line.currency = "USD"
        self.invoice_0kg_1x_1line.kilos = Decimal(0.0)
        self.invoice_0kg_1x_1line.unit = Decimal(1.0)
        self.invoice_0kg_1x_1line.kilos_to_bill.return_value = Decimal(0.0)
        self.invoice_0kg_1x_1line.unit_price.return_value = Decimal(1.0)
        self.invoice_0kg_1x_1line.total = Decimal(1.0)

        self.invoice_1kg_0x_1line = create_autospec(spec=Invoice, instance=True)
        self.invoice_1kg_0x_1line.number = "INV-004"
        self.invoice_1kg_0x_1line.currency = "GBP"
        self.invoice_1kg_0x_1line.kilos = Decimal(1.0)
        self.invoice_1kg_0x_1line.unit = Decimal(0.0)
        self.invoice_1kg_0x_1line.kilos_to_bill.return_value = Decimal(1.0)
        self.invoice_1kg_0x_1line.unit_price.return_value = Decimal(0.0)
        self.invoice_1kg_0x_1line.total = Decimal(1.0)

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
