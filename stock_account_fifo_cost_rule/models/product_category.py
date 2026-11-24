# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    property_fifo_cost_rule = fields.Selection(
        selection=[
            ("average", "Average of remaining layers"),
            ("min", "Lowest remaining cost"),
            ("max", "Highest remaining cost"),
            ("first_in", "Oldest remaining layer"),
            ("last_in", "Latest remaining layer"),
            ("last_out", "Last outgoing cost"),
        ],
        string="FIFO Cost Rule",
        company_dependent=True,
        help="Rule used to set the cost of FIFO products from their valuation layers.",
    )

    def write(self, vals):
        res = super().write(vals)
        if "property_fifo_cost_rule" in vals or "property_cost_method" in vals:
            products = self.env["product.product"].search(
                [("categ_id", "in", self.ids)]
            )
            products._apply_fifo_cost_rule(self.env.company, include_average=True)
        return res
