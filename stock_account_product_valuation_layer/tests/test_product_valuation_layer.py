# Copyright 2026 INVITU (https://www.invitu.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestProductValuationLayer(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Product", "is_storable": True}
        )
        cls.other_product = cls.env["product.product"].create(
            {"name": "Other Product", "is_storable": True}
        )
        cls.layer = cls._create_layer(cls.product)
        cls._create_layer(cls.other_product)

    @classmethod
    def _create_layer(cls, product):
        return cls.env["stock.valuation.layer"].create(
            {
                "product_id": product.id,
                "company_id": cls.env.company.id,
                "quantity": 1.0,
                "unit_cost": 10.0,
                "value": 10.0,
                "remaining_qty": 1.0,
                "remaining_value": 10.0,
            }
        )

    def _layers_from_action(self, action):
        return self.env[action["res_model"]].search(action["domain"])

    def test_product_valuation_layers(self):
        self.assertEqual(self.product.stock_valuation_layer_count, 1)
        action = self.product.action_view_stock_valuation_layers()
        self.assertEqual(self._layers_from_action(action), self.layer)

    def test_template_valuation_layers(self):
        template = self.product.product_tmpl_id
        self.assertEqual(template.stock_valuation_layer_count, 1)
        action = template.action_view_stock_valuation_layers()
        self.assertEqual(self._layers_from_action(action), self.layer)
