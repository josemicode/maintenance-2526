import unittest
from decimal import Decimal

from lab_2_part_2 import (
    CreditNoteBillItem,
    InvoiceLine,
    PartialBilling,
    PriceAdjustmentBillItem,
)


class PartialBillingStub(PartialBilling):
    def __init__(self, billedKg: Decimal = Decimal(0)) -> None:
        self.billedKg = billedKg
        self.barrel = None


class CreditNoteBillItemStub(CreditNoteBillItem):
    def __init__(self, typeDeltaKg: Decimal = Decimal(0)) -> None:
        self.seq = 0
        self.typeDeltaKg = typeDeltaKg
        self.reason = "test"

        self.target = InvoiceLine(
            seq=-1, description="dummy", unitPriceEURPerKg=Decimal(0), qtyKg=Decimal(0)
        )


class PriceAdjustmentBillItemStub(PriceAdjustmentBillItem):
    def __init__(self, deltaUnitPriceEURPerKg: Decimal = Decimal(0)) -> None:
        self.seq = 0
        self.deltaUnitPriceEURPerKg = deltaUnitPriceEURPerKg
        self.qtyBasis = Decimal(0)
        self.deltaTotal = Decimal(0)
        self.reason = "test"

        self.target = InvoiceLine(
            seq=-1, description="dummy", unitPriceEURPerKg=Decimal(0), qtyKg=Decimal(0)
        )


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

        self.partial_not_billed = PartialBillingStub()
        self.partial_20_billed = PartialBillingStub(Decimal(20))
        self.credit_note_no_type = CreditNoteBillItemStub()
        self.credit_note_10_type = CreditNoteBillItemStub(Decimal(10))
        self.price_adj_zero = PriceAdjustmentBillItemStub()
        self.price_adj_1p5 = PriceAdjustmentBillItemStub(Decimal(1.5))
        self.price_adj_2 = PriceAdjustmentBillItemStub(Decimal(2.0))

    def test_add_partial_billing(self) -> None:
        self.invoice_line_20_qty.add_partial_billing(self.partial_not_billed)
        self.assertIn(self.partial_not_billed, self.invoice_line_20_qty.partials)

    def test_add_another_partial_billing(self) -> None:
        self.invoice_line_20_qty.add_partial_billing(self.partial_not_billed)
        self.invoice_line_20_qty.add_partial_billing(self.partial_20_billed)

        self.assertIn(self.partial_not_billed, self.invoice_line_20_qty.partials)
        self.assertIn(self.partial_20_billed, self.invoice_line_20_qty.partials)

    def test_add_credit_note_item(self) -> None:
        self.invoice_line_20_qty.add_credit_note_item(self.credit_note_no_type)
        self.assertIn(
            self.credit_note_no_type, self.invoice_line_20_qty.credit_note_items
        )
        self.assertEqual(self.credit_note_no_type.target, self.invoice_line_20_qty)

    def test_add_another_credit_note_item(self) -> None:
        self.invoice_line_20_qty.add_credit_note_item(self.credit_note_no_type)
        self.invoice_line_20_qty.add_credit_note_item(self.credit_note_10_type)

        self.assertIn(
            self.credit_note_no_type, self.invoice_line_20_qty.credit_note_items
        )
        self.assertIn(
            self.credit_note_10_type, self.invoice_line_20_qty.credit_note_items
        )

    def test_add_price_adjustment_item(self) -> None:
        self.invoice_line_20_qty.add_price_adjustment_item(self.price_adj_zero)
        self.assertIn(
            self.price_adj_zero, self.invoice_line_20_qty.price_adjustment_items
        )
        self.assertEqual(self.price_adj_zero.target, self.invoice_line_20_qty)

    def test_add_another_price_adjustment_item(self) -> None:
        self.invoice_line_20_qty.add_price_adjustment_item(self.price_adj_zero)
        self.invoice_line_20_qty.add_price_adjustment_item(self.price_adj_2)

        self.assertIn(
            self.price_adj_zero, self.invoice_line_20_qty.price_adjustment_items
        )
        self.assertIn(self.price_adj_2, self.invoice_line_20_qty.price_adjustment_items)

    def test_kilos_to_bill_no_remains(self) -> None:
        self.invoice_line_20_qty.add_partial_billing(self.partial_20_billed)
        self.invoice_line_20_qty.add_credit_note_item(self.credit_note_no_type)

        result = self.invoice_line_20_qty.kilos_to_bill()
        self.assertEqual(result, 0)

    def test_kilos_to_bill_negative_remains(self) -> None:
        self.invoice_line_zero_qty.add_partial_billing(self.partial_20_billed)
        self.invoice_line_zero_qty.add_credit_note_item(self.credit_note_10_type)

        result = self.invoice_line_zero_qty.kilos_to_bill()
        self.assertEqual(result, 0)

    def test_kilos_to_bill_remains(self) -> None:
        self.invoice_line_20_qty.add_partial_billing(self.partial_20_billed)
        self.invoice_line_20_qty.add_credit_note_item(self.credit_note_10_type)

        result = self.invoice_line_20_qty.kilos_to_bill()
        self.assertEqual(result, 10)

    def test_unit_price_unchanged(self) -> None:
        self.invoice_line_20_qty.add_price_adjustment_item(self.price_adj_zero)

        unit_price = self.invoice_line_20_qty.unit_price()
        self.assertEqual(unit_price, 2)

    def test_unit_price_updates(self) -> None:
        self.invoice_line_zero_qty.add_price_adjustment_item(self.price_adj_1p5)

        unit_price = self.invoice_line_zero_qty.unit_price()
        self.assertEqual(unit_price, 9)

        self.invoice_line_zero_qty.add_price_adjustment_item(self.price_adj_2)

        unit_price = self.invoice_line_zero_qty.unit_price()
        self.assertEqual(unit_price, 11)
