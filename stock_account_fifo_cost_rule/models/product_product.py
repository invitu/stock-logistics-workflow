# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _apply_fifo_cost_rule(self, company, include_average=False):
        products = self.with_company(company).filtered(
            lambda p: p.cost_method == "fifo"
            and (
                include_average
                or (p.categ_id.property_fifo_cost_rule or "average") != "average"
            )
        )
        if not products:
            return
        Layer = self.env["stock.valuation.layer"].sudo()
        remaining_layers = dict(
            Layer._read_group(
                [
                    ("product_id", "in", products.ids),
                    ("company_id", "=", company.id),
                    ("remaining_qty", ">", 0),
                ],
                ["product_id"],
                ["id:recordset"],
            )
        )
        for product in products:
            rule = product.categ_id.property_fifo_cost_rule or "average"
            if rule == "last_out":
                cost = product._get_fifo_last_out_cost(company)
            else:
                layers = remaining_layers.get(product)
                cost = self._get_fifo_rule_cost(rule, layers) if layers else None
            if cost is None:
                continue
            product.with_context(disable_auto_svl=True).sudo().standard_price = cost

    def _get_fifo_rule_cost(self, rule, layers):
        if rule == "average":
            return sum(layers.mapped("remaining_value")) / sum(
                layers.mapped("remaining_qty")
            )
        layers = layers.sorted(lambda layer: (layer.create_date, layer.id))
        costs = [layer.remaining_value / layer.remaining_qty for layer in layers]
        return {
            "min": min(costs),
            "max": max(costs),
            "first_in": costs[0],
            "last_in": costs[-1],
        }[rule]

    def _get_fifo_last_out_cost(self, company):
        self.ensure_one()
        layer = (
            self.env["stock.valuation.layer"]
            .sudo()
            .search(
                [
                    ("product_id", "=", self.id),
                    ("company_id", "=", company.id),
                    ("quantity", "<", 0),
                    ("stock_move_id", "!=", False),
                ],
                order="create_date desc, id desc",
                limit=1,
            )
        )
        if not layer:
            return None
        # Negative stock corrections are linked to the outgoing layer.
        value = layer.value + sum(layer.stock_valuation_layer_ids.mapped("value"))
        return value / layer.quantity

    def _run_fifo_vacuum(self, company=None):
        res = super()._run_fifo_vacuum(company=company)
        self._apply_fifo_cost_rule(company or self.env.company)
        return res
