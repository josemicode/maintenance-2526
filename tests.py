import unittest
from decimal import Decimal
from sqlite3 import Date

from lab_2_part_1 import (
    BankAccount,
    DateRange,
    Money,
    PasswordPolicy,
    PasswordValidationResult,
    Transaction,
)


class TestMoney(unittest.TestCase):
    def setUp(self) -> None:
        self.item_euro_100 = Money(Decimal(100.0), "Euro")
        self.item_euro_200 = Money(Decimal(200.0), "Euro")
        self.item_dollar_1 = Money(Decimal(1.0), "Dollar")

    def test_addition(self) -> None:
        result: Money = self.item_euro_100.add(self.item_euro_200)
        self.assertEqual(result.amount, Decimal(300.0))

        with self.assertRaises(ValueError):
            self.item_euro_100.add(self.item_dollar_1)

    def test_subtraction(self) -> None:
        result_positive: Money = self.item_euro_200.subtract(self.item_euro_100)
        self.assertEqual(result_positive.amount, Decimal(100.0))

        result_negative: Money = self.item_euro_100.subtract(self.item_euro_200)
        self.assertEqual(result_negative.amount, Decimal(-100.0))

    def test_multiplication(self) -> None:
        result_positive: Money = self.item_euro_100.multiply(5)
        self.assertEqual(result_positive.amount, Decimal(500.0))

        result_negative: Money = self.item_euro_100.multiply(-1)
        self.assertEqual(result_negative.amount, Decimal(-100.0))

        result_zero: Money = self.item_euro_100.multiply(0)
        self.assertEqual(result_zero.amount, 0)

    def test_comparison(self) -> None:
        result_lesser: int = self.item_euro_100.compare_to(self.item_euro_200)
        self.assertEqual(result_lesser, -1)

        result_equal: int = self.item_dollar_1.compare_to(self.item_dollar_1)
        self.assertEqual(result_equal, 0)

        result_greater: int = self.item_euro_200.compare_to(self.item_euro_100)
        self.assertEqual(result_greater, 1)

    def test_equals_operator(self) -> None:
        self.assertTrue(self.item_euro_100 == Money(Decimal(100.0), "Euro"))
        self.assertFalse(self.item_euro_100 == self.item_euro_200)
        self.assertFalse(self.item_euro_100 == self.item_dollar_1)
        self.assertFalse(self.item_euro_100 == "100 Euro")


class TestDateRange(unittest.TestCase):
    def setUp(self) -> None:
        self.item_march_to_may = DateRange(Date(2026, 3, 1), Date(2026, 5, 31))
        self.item_cure = DateRange(Date(1997, 8, 4), Date(1997, 8, 14))
        self.item_matrix = DateRange(Date(2999, 6, 1), Date(2999, 7, 2))
        self.item_10_before_march = DateRange(Date(2026, 2, 19), Date(2026, 3, 1))
        self.item_10_after_may = DateRange(Date(2026, 5, 31), Date(2026, 6, 10))
        self.item_over_march = DateRange(Date(2026, 2, 26), Date(2026, 3, 3))
        self.item_over_may = DateRange(Date(2026, 5, 29), Date(2026, 6, 3))
        self.item_starts_march = DateRange(Date(2026, 3, 1), Date(2026, 3, 10))
        self.item_ends_may = DateRange(Date(2026, 5, 22), Date(2026, 5, 31))
        self.item_april = DateRange(Date(2026, 4, 7), Date(2026, 4, 11))

    def test_contains(self) -> None:
        self.assertTrue(self.item_march_to_may.contains(Date(2026, 4, 7)))
        self.assertTrue(self.item_march_to_may.contains(Date(2026, 3, 1)))
        self.assertTrue(self.item_march_to_may.contains(Date(2026, 5, 31)))

        self.assertFalse(self.item_march_to_may.contains(Date(2026, 2, 14)))
        self.assertFalse(self.item_march_to_may.contains(Date(2026, 12, 1)))

    def test_days_counter(self) -> None:
        self.assertEqual(self.item_cure.days_inclusive(), 11)

    def test_overlaps(self) -> None:
        self.assertTrue(self.item_march_to_may.overlaps(self.item_10_before_march))
        self.assertTrue(self.item_march_to_may.overlaps(self.item_10_after_may))
        self.assertTrue(self.item_march_to_may.overlaps(self.item_over_march))
        self.assertTrue(self.item_march_to_may.overlaps(self.item_over_may))
        self.assertTrue(self.item_march_to_may.overlaps(self.item_starts_march))
        self.assertTrue(self.item_march_to_may.overlaps(self.item_ends_may))
        self.assertTrue(self.item_march_to_may.overlaps(self.item_april))

        self.assertFalse(self.item_march_to_may.overlaps(self.item_cure))
        self.assertFalse(self.item_march_to_may.overlaps(self.item_matrix))

    def test_intersection(self) -> None:
        self.assertEqual(
            self.item_march_to_may.intersection(self.item_10_before_march),
            DateRange(Date(2026, 3, 1), Date(2026, 3, 1)),
        )
        self.assertEqual(
            self.item_march_to_may.intersection(self.item_10_after_may),
            DateRange(Date(2026, 5, 31), Date(2026, 5, 31)),
        )
        self.assertEqual(
            self.item_march_to_may.intersection(self.item_over_march),
            DateRange(Date(2026, 3, 1), Date(2026, 3, 3)),
        )
        self.assertEqual(
            self.item_march_to_may.intersection(self.item_over_may),
            DateRange(Date(2026, 5, 29), Date(2026, 5, 31)),
        )
        self.assertEqual(
            self.item_march_to_may.intersection(self.item_starts_march),
            self.item_starts_march,
        )
        self.assertEqual(
            self.item_march_to_may.intersection(self.item_ends_may), self.item_ends_may
        )
        self.assertEqual(
            self.item_march_to_may.intersection(self.item_april), self.item_april
        )

        self.assertIsNone(self.item_march_to_may.intersection(self.item_cure))
        self.assertIsNone(self.item_march_to_may.intersection(self.item_matrix))

    def test_equality_operator(self) -> None:
        self.assertTrue(
            self.item_april == DateRange(Date(2026, 4, 7), Date(2026, 4, 11))
        )

        self.assertFalse(self.item_cure == self.item_matrix)


class TestPasswordPolicy(unittest.TestCase):
    def setUp(self) -> None:
        self.item_standard = PasswordPolicy()
        self.item_lax = PasswordPolicy(
            min_len=1,
            max_len=20,
            require_upper=False,
            require_digit=False,
            forbid_spaces=False,
        )
        self.item_req_special = PasswordPolicy(require_special=True)

    def test_valid(self) -> None:
        self.assertTrue(self.item_standard.validate("abcdef2G"))
        # self.assertFalse(self.item_standard.validate("abcdef 2G"))

        self.assertTrue(self.item_lax.validate("a b c"))
        # self.assertFalse(self.item_lax.validate("---------------------"))

        self.assertTrue(self.item_req_special.validate("123456_ABC"))
        # self.assertFalse(self.item_req_special.validate("1234567ABC"))

    def test_length(self) -> None:
        self.assertFalse(self.item_standard.validate("1Ac"))
        self.assertFalse(self.item_lax.validate(""))
        self.assertFalse(self.item_req_special.validate("2Bd%"))

        self.assertFalse(self.item_standard.validate("1234567890abcdefG"))
        self.assertFalse(self.item_lax.validate("---------------------"))
        self.assertFalse(self.item_req_special.validate("abcdeF-1234567890"))

    def test_missing(self) -> None:
        self.assertFalse(self.item_standard.validate("abcdefgh1$"))
        self.assertTrue(self.item_lax.validate("abcdefgh1$"))
        self.assertFalse(self.item_req_special.validate("abcdefgh1$"))

        self.assertFalse(self.item_standard.validate("Abcdefgh$"))
        self.assertTrue(self.item_lax.validate("Abcdefgh$"))
        self.assertFalse(self.item_req_special.validate("Abcdefgh$"))

        self.assertTrue(self.item_standard.validate("Abcdefg1"))
        self.assertTrue(self.item_lax.validate("Abcdefg1"))
        self.assertFalse(self.item_req_special.validate("Abcdefg1"))

    def test_spaces(self) -> None:
        self.assertFalse(self.item_standard.validate("Abcd efgh1$"))
        self.assertTrue(self.item_lax.validate("Abcd efgh1$"))
        self.assertFalse(self.item_req_special.validate("Abcd efgh1$"))

    def test_multiple_infractions(self) -> None:
        result_no_errors: PasswordValidationResult = self.item_req_special.validate(
            "Abcdefgh1$"
        )
        error_count = len(result_no_errors.errors)
        self.assertEqual(error_count, 0)

        result_one_error: PasswordValidationResult = self.item_lax.validate(
            "Abcdefgh1$ abcabcabcabc"
        )
        error_count = len(result_one_error.errors)
        self.assertEqual(error_count, 1)

        result_multiple_errors: PasswordValidationResult = self.item_standard.validate(
            "yoda"
        )
        error_count = len(result_multiple_errors.errors)
        self.assertEqual(error_count, 3)


class TestBankAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.item_standard = BankAccount(Decimal(2000))
        self.item_standard.deposit(Decimal(300))
        self.item_standard.withdraw(Decimal(100))
        self.item_new_account = BankAccount()

    def test_deposit(self) -> None:
        self.item_new_account.deposit(Decimal(100))
        self.item_standard.deposit(Decimal(300))

        self.assertEqual(self.item_new_account.get_balance(), 100)
        self.assertEqual(self.item_standard.get_balance(), 2500)
        self.assertEqual(len(self.item_new_account.get_statement()), 1)
        self.assertEqual(len(self.item_standard.get_statement()), 3)

    def test_withdraw(self) -> None:
        with self.assertRaises(ValueError):
            self.item_new_account.withdraw(Decimal(100))
        self.item_standard.withdraw(Decimal(300))

        self.assertNotEqual(self.item_new_account.get_balance(), -100)
        self.assertEqual(self.item_standard.get_balance(), 1900)
        self.assertEqual(len(self.item_new_account.get_statement()), 0)
        self.assertEqual(len(self.item_standard.get_statement()), 3)

    def test_modify_statement(self) -> None:
        statement = self.item_standard.get_statement()
        transaction = Transaction("deposit", Decimal(5000), "Not suspicious at all")

        with self.assertRaises(TypeError):
            statement[1] = transaction

    def test_invalid_transaction(self) -> None:
        with self.assertRaises(ValueError):
            self.item_new_account.deposit(Decimal(-13))
        with self.assertRaises(ValueError):
            self.item_new_account.deposit(Decimal(0))

        with self.assertRaises(ValueError):
            self.item_standard.withdraw(Decimal(-600))
        with self.assertRaises(ValueError):
            self.item_standard.withdraw(Decimal(0))


class TestShoppingCart(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_invalid(self) -> None:
        qty_string, price_negative = "two", Decimal(-13)

        with self.assertRaises(ValueError):
            self.item_base_cart.add_item(
                sku="Impossible", unit_price=price_negative, qty=1
            )

        with self.assertRaises(TypeError):
            self.item_base_cart.add_item(sku="2", unit_price=Decimal(2), qty=qty_string)
