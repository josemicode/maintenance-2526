import unittest
from decimal import Decimal
from sqlite3 import Date

from lab_2_part_1 import (
    BankAccount,
    CartItem,
    DateRange,
    LRUCache,
    Money,
    PalindromeChecker,
    PasswordPolicy,
    PasswordValidationResult,
    ShoppingCart,
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
        self.item_base_cart = ShoppingCart()
        self.item_half_off = ShoppingCart(discount_percent=Decimal(50))
        self.item_dummy_element = CartItem(sku="Dummy", unit_price=Decimal(5), qty=1)
        self.item_four_elements = CartItem(sku="Box", unit_price=Decimal(2), qty=4)
        self.item_pie_element = CartItem(sku="Pie", unit_price=Decimal(3.141592), qty=1)

    def _cartitem_to_dict(self, cart_item: CartItem) -> dict:
        return {
            "sku": cart_item.sku,
            "unit_price": cart_item.unit_price,
            "qty": cart_item.qty,
        }

    def test_single_compute(self) -> None:
        self.item_base_cart.add_item(**self._cartitem_to_dict(self.item_dummy_element))
        subtotal = self.item_base_cart.subtotal()

        self.assertEqual(subtotal, 5)

    def test_quantity_post_addition(self) -> None:
        self.item_base_cart.add_item(**self._cartitem_to_dict(self.item_dummy_element))
        self.item_base_cart.add_item(**self._cartitem_to_dict(self.item_dummy_element))

        self.assertEqual(self.item_base_cart.total_items(), 2)

    def test_removal(self) -> None:
        self.item_base_cart.add_item(**self._cartitem_to_dict(self.item_dummy_element))
        self.item_base_cart.add_item(**self._cartitem_to_dict(self.item_four_elements))
        self.item_base_cart.remove_sku(self.item_dummy_element.sku)

        self.assertNotIn(self.item_dummy_element, self.item_base_cart.items())

    def test_discount(self) -> None:
        self.item_half_off.add_item(**self._cartitem_to_dict(self.item_pie_element))
        # self.assertEqual(self.item_half_off.total(), 4)
        self.assertEqual(self.item_half_off.total(), Decimal("1.57"))

    def test_invalid(self) -> None:
        qty_string, price_negative = "two", Decimal(-13)

        with self.assertRaises(ValueError):
            self.item_base_cart.add_item(
                sku="Impossible", unit_price=price_negative, qty=1
            )

        with self.assertRaises(TypeError):
            self.item_base_cart.add_item(sku="2", unit_price=Decimal(2), qty=qty_string)


class TestLRUCache(unittest.TestCase):
    def setUp(self) -> None:
        self.item_size_1 = LRUCache[int, str](1)
        self.item_size_2 = LRUCache[int, str](2)
        self.item_size_3 = LRUCache[int, str](3)
        self.item_size_4 = LRUCache[int, str](4)

    def test_initialization(self) -> None:
        cache = LRUCache[int, str](5)
        self.assertEqual(cache.size(), 0)
        self.assertFalse(cache.contains_key(1))

        with self.assertRaises(TypeError):
            LRUCache[int, str]("invalid")
        with self.assertRaises(ValueError):
            LRUCache[int, str](0)
        with self.assertRaises(ValueError):
            LRUCache[int, str](-1)

    def test_basic_put_and_get(self) -> None:
        self.item_size_3.put(1, "one")
        self.item_size_3.put(2, "two")

        self.assertEqual(self.item_size_3.get(1), "one")
        self.assertEqual(self.item_size_3.get(2), "two")
        self.assertEqual(self.item_size_3.size(), 2)

    def test_get_nonexistent_key(self) -> None:
        self.assertIsNone(self.item_size_3.get(1))
        self.assertFalse(self.item_size_3.contains_key(1))

    def test_contains_key(self) -> None:
        self.item_size_3.put(1, "one")
        self.assertTrue(self.item_size_3.contains_key(1))
        self.assertFalse(self.item_size_3.contains_key(2))

    def test_capacity_constraints(self) -> None:
        self.item_size_2.put(1, "one")
        self.item_size_2.put(2, "two")
        self.assertEqual(self.item_size_2.size(), 2)

        self.item_size_2.put(3, "three")
        self.assertEqual(self.item_size_2.size(), 2)

    def test_eviction_behavior(self) -> None:
        self.item_size_2.put(1, "one")
        self.item_size_2.put(2, "two")

        self.item_size_2.put(3, "three")

        self.assertEqual(self.item_size_2.size(), 2)
        self.assertIsNone(self.item_size_2.get(1))
        self.assertEqual(self.item_size_2.get(2), "two")
        self.assertEqual(self.item_size_2.get(3), "three")

    def test_recency_updates_on_get(self) -> None:
        self.item_size_3.put(1, "one")
        self.item_size_3.put(2, "two")
        self.item_size_3.put(3, "three")

        self.item_size_3.get(1)

        self.item_size_3.put(4, "four")

        self.assertEqual(self.item_size_3.size(), 3)
        self.assertIsNone(self.item_size_3.get(2))
        self.assertEqual(self.item_size_3.get(1), "one")
        self.assertEqual(self.item_size_3.get(3), "three")
        self.assertEqual(self.item_size_3.get(4), "four")

    def test_recency_updates_on_put_existing(self) -> None:

        self.item_size_3.put(1, "one")
        self.item_size_3.put(2, "two")
        self.item_size_3.put(3, "three")

        self.item_size_3.put(1, "one_updated")

        self.item_size_3.put(4, "four")

        self.assertEqual(self.item_size_3.size(), 3)
        self.assertIsNone(self.item_size_3.get(2))
        self.assertEqual(self.item_size_3.get(1), "one_updated")
        self.assertEqual(self.item_size_3.get(3), "three")
        self.assertEqual(self.item_size_3.get(4), "four")

    def test_keys_mru_order(self) -> None:

        self.item_size_3.put(1, "one")
        self.item_size_3.put(2, "two")
        self.item_size_3.put(3, "three")

        self.assertEqual(self.item_size_3.keys_mru_order(), (1, 2, 3))

        self.item_size_3.get(1)
        self.assertEqual(self.item_size_3.keys_mru_order(), (2, 3, 1))

        self.item_size_3.put(2, "two_updated")
        self.assertEqual(self.item_size_3.keys_mru_order(), (3, 1, 2))

    def test_complex_eviction_scenario(self) -> None:
        self.item_size_3.put(1, "one")
        self.item_size_3.put(2, "two")
        self.item_size_3.put(3, "three")

        self.item_size_3.get(1)
        self.item_size_3.get(2)
        self.item_size_3.get(3)
        self.item_size_3.get(1)

        self.item_size_3.put(4, "four")

        self.assertEqual(self.item_size_3.size(), 3)
        self.assertIsNone(self.item_size_3.get(2))
        self.assertEqual(self.item_size_3.keys_mru_order(), (3, 1, 4))

        self.assertEqual(self.item_size_3.get(1), "one")
        self.assertEqual(self.item_size_3.get(3), "three")
        self.assertEqual(self.item_size_3.get(4), "four")

    def test_update_value_same_key(self) -> None:
        self.item_size_3.put(1, "one")
        self.item_size_3.put(2, "two")

        self.assertEqual(self.item_size_3.size(), 2)
        self.assertEqual(self.item_size_3.get(1), "one")

        self.item_size_3.put(1, "one_updated")

        self.assertEqual(self.item_size_3.size(), 2)
        self.assertEqual(self.item_size_3.get(1), "one_updated")
        self.assertEqual(self.item_size_3.get(2), "two")

    def test_edge_case_single_capacity(self) -> None:
        self.item_size_1.put(1, "one")
        self.assertEqual(self.item_size_1.size(), 1)
        self.assertEqual(self.item_size_1.get(1), "one")

        self.item_size_1.put(2, "two")
        self.assertEqual(self.item_size_1.size(), 1)
        self.assertIsNone(self.item_size_1.get(1))
        self.assertEqual(self.item_size_1.get(2), "two")

        self.item_size_1.get(2)
        self.item_size_1.put(3, "three")
        self.assertIsNone(self.item_size_1.get(2))
        self.assertEqual(self.item_size_1.get(3), "three")

    def test_mixed_operations(self) -> None:
        self.item_size_4.put(1, "a")
        self.item_size_4.put(2, "b")
        self.item_size_4.put(3, "c")

        self.item_size_4.get(1)
        self.item_size_4.put(2, "b_updated")
        self.item_size_4.put(4, "d")

        self.item_size_4.put(5, "e")

        self.assertEqual(self.item_size_4.size(), 4)
        self.assertIsNone(self.item_size_4.get(3))
        self.assertEqual(self.item_size_4.get(1), "a")
        self.assertEqual(self.item_size_4.get(2), "b_updated")
        self.assertEqual(self.item_size_4.get(4), "d")
        self.assertEqual(self.item_size_4.get(5), "e")

        self.assertEqual(self.item_size_4.keys_mru_order(), (1, 2, 4, 5))


class TestPalindromeChecker(unittest.TestCase):
    def setUp(self) -> None:
        self.item_restrictive = PalindromeChecker(
            ignore_case=False, ignore_spaces=False, ignore_punctuation=False
        )
        self.item_case_agnostic = PalindromeChecker(
            ignore_case=True, ignore_spaces=False, ignore_punctuation=False
        )
        self.item_space_agnostic = PalindromeChecker(
            ignore_case=False, ignore_spaces=True, ignore_punctuation=False
        )
        self.item_punct_agnostic = PalindromeChecker(
            ignore_case=False, ignore_spaces=False, ignore_punctuation=True
        )
        self.item_all_agnostic = PalindromeChecker(
            ignore_case=True, ignore_spaces=True, ignore_punctuation=True
        )

    def test_input_validation(self) -> None:
        with self.assertRaises(TypeError):
            self.item_restrictive.normalize(121)

    def test_normalize_spaces(self) -> None:
        """Test that spaces are normalized according to configuration"""
        # Test with ignore_spaces=True (default)
        result = self.item_space_agnostic.normalize("a b c")
        self.assertEqual(result, "abc")

        # Test with ignore_spaces=False
        result = self.item_restrictive.normalize("a b c")
        self.assertEqual(result, "a b c")

        # Test with different types of whitespace
        result = self.item_space_agnostic.normalize("a\tb\nc")
        self.assertEqual(result, "abc")

        # Test mixed configuration
        checker = PalindromeChecker(
            ignore_case=True, ignore_spaces=True, ignore_punctuation=False
        )
        result = checker.normalize("A B C!")
        self.assertEqual(result, "abc!")

    def test_normalize_punctuation(self) -> None:
        """Test that punctuation is normalized according to configuration"""
        # Test with ignore_punctuation=True
        result = self.item_punct_agnostic.normalize("a,b.c!")
        self.assertEqual(result, "abc")

        # Test with ignore_punctuation=False
        result = self.item_restrictive.normalize("a,b.c!")
        self.assertEqual(result, "a,b.c!")

        # Test various punctuation characters
        result = self.item_punct_agnostic.normalize("a@b#c$d%e^f&g*h(i)j")
        self.assertEqual(result, "abcdefghij")

        # Test that spaces are preserved when ignore_punctuation=True but ignore_spaces=False
        checker = PalindromeChecker(
            ignore_case=False, ignore_spaces=False, ignore_punctuation=True
        )
        result = checker.normalize("a, b. c!")
        self.assertEqual(result, "a b c")

    def test_normalize_case(self) -> None:
        """Test that case is normalized according to configuration"""
        # Test with ignore_case=True (default)
        result = self.item_case_agnostic.normalize("AbC")
        self.assertEqual(result, "abc")

        # Test with ignore_case=False
        result = self.item_restrictive.normalize("AbC")
        self.assertEqual(result, "AbC")

        # Test mixed case with spaces and punctuation
        checker = PalindromeChecker(
            ignore_case=True, ignore_spaces=True, ignore_punctuation=True
        )
        result = checker.normalize("A b, C!")
        self.assertEqual(result, "abc")