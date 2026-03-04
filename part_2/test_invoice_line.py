import unittest
from decimal import Decimal

from lab_2_part_2 import CreditNoteBillItem, Invoice, InvoiceLine, PartialBilling


class PartialBillingStub(PartialBilling):
    def __init__(self, billedKg: Decimal = Decimal(0)) -> None:
        self.billedKg = billedKg


class CreditNoteBillItemStub(CreditNoteBillItem):
    #!FIXME
    def __init__(self, typeDeltaKg: Decimal = Decimal(0), target: InvoiceLine,) -> None:
        self.typeDeltaKg = typeDeltaKg
        self.target = target


class PriceAdjustmentBillItem:
    pass


class TestInvoiceLine(unittest.TestCase):
    def setUp(self) -> None:
        self.invoice_line_20_qty = InvoiceLine(
            seq=1, description="Line X", unitPriceEURPerKg=Decimal(2), qtyKg=Decimal(20)
        )

        self.partial_not_billed = PartialBillingStub()
        self.partial_20_billed = PartialBillingStub(Decimal(20))
        self.credit_note_no_type = CreditNoteBillItemStub()
        self.credit_note_10_type = CreditNoteBillItemStub(Decimal(10))

    def test_partial_billing(self) -> None:
        self.invoice_line_20_qty.add_partial_billing(self.partial_not_billed)
        self.assertIn(self.partial_not_billed, self.invoice_line_20_qty.partials)

    def test_add_credit_note_item(self) -> None:
        self.invoice_line_20_qty.add_credit_note_item(self.credit_note_no_type)
        self.assertIn(
            self.credit_note_no_type, self.invoice_line_20_qty.credit_note_items
        )
