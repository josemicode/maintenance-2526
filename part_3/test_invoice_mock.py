import unittest
from datetime import date
from decimal import Decimal
from unittest.mock import Mock

from lab_2_part_3 import Invoice, InvoiceLine


class TestInvoice(unittest.TestCase):
    def setUp(self) -> None:
        self.invoice_eur = Invoice(number="INV-013", date=date.today(), currency="EUR")

        self.inv_line_50_kg = Mock(spec=InvoiceLine)
        self.inv_line_50_kg.seq = 1
        self.inv_line_50_kg.description = "Line C"
        self.inv_line_50_kg.unitPriceEURPerKg = Decimal(1.0)
        self.inv_line_50_kg.qtyKg = Decimal(50.0)
        self.inv_line_50_kg.lineAmount = Decimal(10.0)
        self.inv_line_50_kg.kilos_to_bill.return_value = Decimal(50.0)
        self.inv_line_50_kg.unit_price.return_value = Decimal(1.0)

        self.inv_line_100_kg_price_x2 = Mock(spec=InvoiceLine)
        self.inv_line_100_kg_price_x2.seq = 2
        self.inv_line_100_kg_price_x2.description = "Line D"
        self.inv_line_100_kg_price_x2.unitPriceEURPerKg = Decimal(2.0)
        self.inv_line_100_kg_price_x2.qtyKg = Decimal(100.0)
        self.inv_line_100_kg_price_x2.lineAmount = Decimal(10.0)
        self.inv_line_100_kg_price_x2.kilos_to_bill.return_value = Decimal(100.0)
        self.inv_line_100_kg_price_x2.unit_price.return_value = Decimal(2.0)

    def test_add_line(self) -> None:
        self.invoice_eur.add_line(self.inv_line_50_kg)
        self.assertIn(self.inv_line_50_kg, self.invoice_eur.lines)

    def test_add_another_line(self) -> None:
        self.invoice_eur.add_line(self.inv_line_50_kg)
        self.invoice_eur.add_line(self.inv_line_100_kg_price_x2)

        self.assertIn(self.inv_line_50_kg, self.invoice_eur.lines)
        self.assertIn(self.inv_line_100_kg_price_x2, self.invoice_eur.lines)

    def test_kilos_to_bill_no_line(self) -> None:
        result = self.invoice_eur.kilos_to_bill()
        self.assertEqual(result, 0)

    def test_kilos_to_bill(self) -> None:
        self.invoice_eur.add_line(self.inv_line_50_kg)
        self.invoice_eur.add_line(self.inv_line_100_kg_price_x2)

        result = self.invoice_eur.kilos_to_bill()
        self.assertEqual(result, 150)

    def test_unit_price_no_line(self) -> None:
        result = self.invoice_eur.unit_price()
        self.assertEqual(result, 0)

    def test_unit_price(self) -> None:
        self.invoice_eur.add_line(self.inv_line_50_kg)

        result = self.invoice_eur.unit_price()
        self.assertEqual(result, 1)

        self.invoice_eur.add_line(self.inv_line_100_kg_price_x2)

        result = self.invoice_eur.unit_price()
        self.assertAlmostEqual(result, Decimal("1.6666667"))

    def test_total_no_line(self) -> None:
        self.assertEqual(self.invoice_eur.total, 0)

    def test_total(self) -> None:
        self.invoice_eur.add_line(self.inv_line_50_kg)
        self.assertEqual(self.invoice_eur.total, 10)

        self.invoice_eur.add_line(self.inv_line_100_kg_price_x2)
        self.assertEqual(self.invoice_eur.total, 20)
