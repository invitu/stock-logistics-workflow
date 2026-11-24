# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import tagged

from odoo.addons.stock_account.tests.test_stockvaluationlayer import (
    TestStockValuationCommon,
)


@tagged("post_install", "-at_install")
class TestFifoCostRule(TestStockValuationCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env["product.category"].create(
            {
                "name": "FIFO",
                "property_cost_method": "fifo",
                "property_valuation": "manual_periodic",
            }
        )
        cls.product1.categ_id = cls.category

    def test_max(self):
        self.category.property_fifo_cost_rule = "max"
        self._make_in_move(self.product1, 1, unit_cost=15)
        self._make_in_move(self.product1, 1, unit_cost=10)
        self.assertEqual(self.product1.standard_price, 15)
        self._make_out_move(self.product1, 1)
        self.assertEqual(self.product1.standard_price, 10)

    def test_min(self):
        self.category.property_fifo_cost_rule = "min"
        self._make_in_move(self.product1, 1, unit_cost=10)
        self._make_in_move(self.product1, 1, unit_cost=15)
        self.assertEqual(self.product1.standard_price, 10)
        self._make_out_move(self.product1, 1)
        self.assertEqual(self.product1.standard_price, 15)

    def test_first_in_last_in(self):
        self.category.property_fifo_cost_rule = "first_in"
        self._make_in_move(self.product1, 1, unit_cost=10)
        self._make_in_move(self.product1, 1, unit_cost=15)
        self.assertEqual(self.product1.standard_price, 10)
        self.category.property_fifo_cost_rule = "last_in"
        self.assertEqual(self.product1.standard_price, 15)

    def test_last_out(self):
        self.category.property_fifo_cost_rule = "last_out"
        self._make_in_move(self.product1, 1, unit_cost=10)
        self._make_in_move(self.product1, 1, unit_cost=15)
        self._make_out_move(self.product1, 1)
        self.assertEqual(self.product1.standard_price, 10)
        self._make_in_move(self.product1, 1, unit_cost=20)
        self.assertEqual(self.product1.standard_price, 10)

    def test_rule_change(self):
        self._make_in_move(self.product1, 1, unit_cost=10)
        self._make_in_move(self.product1, 1, unit_cost=15)
        self.assertEqual(self.product1.standard_price, 12.5)
        self.category.property_fifo_cost_rule = "max"
        self.assertEqual(self.product1.standard_price, 15)
        self.category.property_fifo_cost_rule = "average"
        self.assertEqual(self.product1.standard_price, 12.5)
