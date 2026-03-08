from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List, Optional, Union

# -----------------------
# Low-level value objects
# -----------------------


@dataclass(slots=True, frozen=True)
class Barrel:
    code: str
    netKg: Decimal


@dataclass(slots=True)
class PartialBilling:
    billedKg: Decimal
    barrel: Optional[Barrel] = None


# -----------------------
# Forward declarations (for type hints)
# -----------------------
# (Defined later; used for annotations inside InvoiceLine)
class CreditNoteBillItem: ...


class PriceAdjustmentBillItem: ...


# -----------------------
# Core domain: Invoice / lines
# -----------------------


@dataclass
class InvoiceLine:
    seq: int
    description: str
    unitPriceEURPerKg: Decimal
    qtyKg: Decimal

    partials: List[PartialBilling] = field(default_factory=list)
    credit_note_items: List[CreditNoteBillItem] = field(
        default_factory=list, repr=False
    )
    price_adjustment_items: List[PriceAdjustmentBillItem] = field(
        default_factory=list, repr=False
    )

    # ---- relationship management helpers ----

    def add_partial_billing(self, partial: PartialBilling) -> None:
        self.partials.append(partial)

    def add_credit_note_item(self, item: CreditNoteBillItem) -> None:
        """
        Adds an item and enforces the bidirectional link.
        """
        if item.target is not self:
            item.target = self
        if item not in self.credit_note_items:
            self.credit_note_items.append(item)

    def add_price_adjustment_item(self, item: PriceAdjustmentBillItem) -> None:
        """
        Adds an item and enforces the bidirectional link.
        """
        if item.target is not self:
            item.target = self
        if item not in self.price_adjustment_items:
            self.price_adjustment_items.append(item)

    # ---- business logic ----

    def kilos_to_bill(self) -> Decimal:
        """
        Depends on current PartialBillings and CreditNoteBillItems.
        remaining = qty - already_billed + sum(credit_deltas)
        clamped at 0
        """
        already_billed = sum((p.billedKg for p in self.partials), Decimal("0"))
        credit_delta = sum(
            (i.typeDeltaKg for i in self.credit_note_items), Decimal("0")
        )
        remaining = self.qtyKg - already_billed + credit_delta
        return max(Decimal("0"), remaining)

    def unit_price(self) -> Decimal:
        """
        Depends on PriceAdjustmentBillItems.
        effective = base + sum(price_deltas)
        """
        delta = sum(
            (i.deltaUnitPriceEURPerKg for i in self.price_adjustment_items),
            Decimal("0"),
        )
        return self.unitPriceEURPerKg + delta

    @property
    def lineAmount(self) -> Decimal:
        """
        Derived: billable kilos * effective unit price.
        """
        return self.kilos_to_bill() * self.unit_price()


@dataclass
class Invoice:
    number: str
    date: date
    currency: str

    lines: List[InvoiceLine] = field(default_factory=list)

    # ---- relationship management helpers ----

    def add_line(self, line: InvoiceLine) -> None:
        if line not in self.lines:
            self.lines.append(line)

    # ---- business logic ----

    def kilos_to_bill(self) -> Decimal:
        return sum((line.kilos_to_bill() for line in self.lines), Decimal("0"))

    def unit_price(self) -> Decimal:
        """
        Example derived invoice unit price: weighted average by billable kilos.
        Change if your domain uses a different rule.
        """
        total_kilos = self.kilos_to_bill()
        if total_kilos == 0:
            return Decimal("0")
        weighted_sum = sum(
            (line.unit_price() * line.kilos_to_bill() for line in self.lines),
            Decimal("0"),
        )
        return weighted_sum / total_kilos

    @property
    def total(self) -> Decimal:
        return sum((line.lineAmount for line in self.lines), Decimal("0"))


# -----------------------
# Credit note / items
# -----------------------


@dataclass
class CreditNoteBillItem:
    seq: int
    typeDeltaKg: Decimal
    reason: str
    target: InvoiceLine

    def __post_init__(self) -> None:
        # Ensure inverse relationship
        self.target.add_credit_note_item(self)


@dataclass
class CreditNote:
    number: str
    date: date
    currency: str

    items: List[CreditNoteBillItem] = field(default_factory=list)

    # ---- relationship management helpers ----

    def add_item(self, item: CreditNoteBillItem) -> None:
        if item not in self.items:
            self.items.append(item)
        # Ensure inverse relationship (idempotent)
        item.target.add_credit_note_item(item)

    @property
    def total(self) -> Decimal:
        """
        Placeholder derived total:
        sum(deltaKg * target.effective_unit_price)

        NOTE: Real accounting may treat credit notes as negative totals, etc.
        Adjust sign conventions as needed.
        """
        return sum(
            (item.typeDeltaKg * item.target.unit_price() for item in self.items),
            Decimal("0"),
        )


# -----------------------
# Price adjustment / items
# -----------------------


@dataclass
class PriceAdjustmentBillItem:
    seq: int
    deltaUnitPriceEURPerKg: Decimal
    qtyBasis: Decimal
    deltaTotal: Decimal
    reason: str
    target: InvoiceLine

    def __post_init__(self) -> None:
        # Ensure inverse relationship
        self.target.add_price_adjustment_item(self)


@dataclass
class PriceAdjustmentBill:
    number: str
    date: date
    currency: str

    items: List[PriceAdjustmentBillItem] = field(default_factory=list)

    # ---- relationship management helpers ----

    def add_item(self, item: PriceAdjustmentBillItem) -> None:
        if item not in self.items:
            self.items.append(item)
        # Ensure inverse relationship (idempotent)
        item.target.add_price_adjustment_item(item)

    @property
    def total(self) -> Decimal:
        return sum((item.deltaTotal for item in self.items), Decimal("0"))


# -----------------------
# Provider + Bills
# -----------------------

Bill = Union[Invoice, CreditNote, PriceAdjustmentBill]


@dataclass
class Provider:
    """
    Provider has a list of bills (Invoice, CreditNote, PriceAdjustmentBill).
    """

    name: str
    bills: List[Bill] = field(default_factory=list)

    # ---- relationship management helpers ----

    def add_bill(self, bill: Bill) -> None:
        if bill not in self.bills:
            self.bills.append(bill)

    def invoices(self) -> List[Invoice]:
        return [b for b in self.bills if isinstance(b, Invoice)]

    def credit_notes(self) -> List[CreditNote]:
        return [b for b in self.bills if isinstance(b, CreditNote)]

    def price_adjustment_bills(self) -> List[PriceAdjustmentBill]:
        return [b for b in self.bills if isinstance(b, PriceAdjustmentBill)]

    # ---- business queries (examples) ----

    def total_kilos_to_bill(self) -> Decimal:
        """
        Sum kilos_to_bill across all invoices.
        """
        return sum((inv.kilos_to_bill() for inv in self.invoices()), Decimal("0"))

    def avg_unit_price(self) -> Decimal:
        """
        Weighted average unit price across all invoices by their billable kilos.
        """
        invoices = self.invoices()
        total_kilos = sum((inv.kilos_to_bill() for inv in invoices), Decimal("0"))
        if total_kilos == 0:
            return Decimal("0")
        weighted_sum = sum(
            (inv.unit_price() * inv.kilos_to_bill() for inv in invoices), Decimal("0")
        )
        return weighted_sum / total_kilos

    def total_invoice_amount(self) -> Decimal:
        return sum((inv.total for inv in self.invoices()), Decimal("0"))


# -----------------------
# Example wiring (optional)
# -----------------------

if __name__ == "__main__":
    provider = Provider(name="ACME Provider")

    inv = Invoice(number="INV-001", date=date.today(), currency="EUR")
    line1 = InvoiceLine(
        seq=1,
        description="Line A",
        unitPriceEURPerKg=Decimal("2.00"),
        qtyKg=Decimal("100"),
    )
    line2 = InvoiceLine(
        seq=2,
        description="Line B",
        unitPriceEURPerKg=Decimal("3.00"),
        qtyKg=Decimal("50"),
    )

    inv.add_line(line1)
    inv.add_line(line2)

    # Partials
    line1.add_partial_billing(
        PartialBilling(
            billedKg=Decimal("30"), barrel=Barrel(code="B1", netKg=Decimal("30"))
        )
    )

    # Credit note affecting line1
    cn = CreditNote(number="CN-001", date=date.today(), currency="EUR")
    cn_item = CreditNoteBillItem(
        seq=1, typeDeltaKg=Decimal("-10"), reason="Return", target=line1
    )
    cn.add_item(cn_item)

    # Price adjustment affecting line2
    pab = PriceAdjustmentBill(number="PAB-001", date=date.today(), currency="EUR")
    pa_item = PriceAdjustmentBillItem(
        seq=1,
        deltaUnitPriceEURPerKg=Decimal("0.50"),
        qtyBasis=Decimal("50"),
        deltaTotal=Decimal("25.00"),
        reason="Surcharge",
        target=line2,
    )
    pab.add_item(pa_item)

    provider.add_bill(inv)
    provider.add_bill(cn)
    provider.add_bill(pab)

    print("Provider total kilos_to_bill:", provider.total_kilos_to_bill())
    print("Provider avg unit price:", provider.avg_unit_price())
    print("Provider total invoice amount:", provider.total_invoice_amount())
    print("Invoice total:", inv.total)
    print("CreditNote total:", cn.total)
    print("PriceAdjustmentBill total:", pab.total)
