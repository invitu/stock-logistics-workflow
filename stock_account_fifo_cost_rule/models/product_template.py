# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        res = super().write(vals)
        if "categ_id" in vals:
            self.product_variant_ids._apply_fifo_cost_rule(
                self.env.company, include_average=True
            )
        return res
