from decimal import Decimal

from django.test import SimpleTestCase

from .services import per_child_amount


class PerChildAmountTests(SimpleTestCase):
    def test_divides_evenly(self):
        result = per_child_amount(Decimal(50000), Decimal(0), 25, Decimal(100))
        self.assertEqual(result, Decimal(2000))

    def test_rounds_up_to_step(self):
        # 50000 / 23 = 2173.91 -> 2200
        result = per_child_amount(Decimal(50000), Decimal(0), 23, Decimal(100))
        self.assertEqual(result, Decimal(2200))

    def test_piggy_bank_reduces_amount(self):
        # (50000 - 10000) / 20 = 2000
        result = per_child_amount(Decimal(50000), Decimal(10000), 20, Decimal(100))
        self.assertEqual(result, Decimal(2000))

    def test_rounding_step_500(self):
        # 50000 / 23 = 2173.91 -> 2500
        result = per_child_amount(Decimal(50000), Decimal(0), 23, Decimal(500))
        self.assertEqual(result, Decimal(2500))

    def test_zero_participants_is_error(self):
        with self.assertRaises(ValueError):
            per_child_amount(Decimal(50000), Decimal(0), 0, Decimal(100))

    def test_piggy_more_than_cost_is_error(self):
        with self.assertRaises(ValueError):
            per_child_amount(Decimal(1000), Decimal(2000), 10, Decimal(100))
