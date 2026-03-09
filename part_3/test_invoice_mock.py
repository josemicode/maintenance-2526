import unittest


class TestInvoice(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

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
