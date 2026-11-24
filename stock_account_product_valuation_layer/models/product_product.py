# Copyright 2026 INVITU (https://www.invitu.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    stock_valuation_layer_count = fields.Integer(
        compute="_compute_stock_valuation_layer_count",
        groups="stock.group_stock_manager",
    )

    def _get_stock_valuation_layer_domain(self):
        return [("product_id", "in", self.ids)]

    def _compute_stock_valuation_layer_count(self):
        counts = dict(
            self.env["stock.valuation.layer"]._read_group(
                self._get_stock_valuation_layer_domain(),
                ["product_id"],
                ["__count"],
            )
        )
        for product in self:
            product.stock_valuation_layer_count = counts.get(product._origin, 0)

    def action_view_stock_valuation_layers(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock_account.stock_valuation_layer_action"
        )
        action["domain"] = self._get_stock_valuation_layer_domain()
        return action
