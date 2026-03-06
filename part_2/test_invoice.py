import unittest
from datetime import date
from decimal import Decimal

from lab_2_part_2 import Invoice


class InvoiceLineStub:
    def __init__(
        self,
        seq: int,
        description: str,
        unitPriceEURPerKg: Decimal,
        qtyKg: Decimal,
        lineAmount: int,
    ) -> None:
        self.seq = seq
        self.description = description
        self.unitPriceEURPerKg = unitPriceEURPerKg
        self.qtyKg = qtyKg
        self.lineAmount = lineAmount

    def kilos_to_bill(self) -> Decimal:
        return self.qtyKg


class TestInvoice(unittest.TestCase):
    def setUp(self) -> None:
        self.invoice_eur = Invoice(number="INV-013", date=date.today(), currency="EUR")
        self.inv_line_50_kg = InvoiceLineStub(
            seq=1,
            description="Line C",
            unitPriceEURPerKg=Decimal(1.0),
            qtyKg=Decimal(50.0),
            lineAmount=10,
        )

        self.inv_line_100_kg_price_x2 = InvoiceLineStub(
            seq=2,
            description="Line D",
            unitPriceEURPerKg=Decimal(2.0),
            qtyKg=Decimal(100.0),
            lineAmount=10,
        )

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
