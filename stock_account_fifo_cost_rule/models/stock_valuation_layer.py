# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    def _apply_fifo_cost_rule(self):
        for company, layers in self.grouped("company_id").items():
            layers.product_id._apply_fifo_cost_rule(company)
