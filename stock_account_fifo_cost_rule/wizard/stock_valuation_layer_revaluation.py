# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class StockValuationLayerRevaluation(models.TransientModel):
    _inherit = "stock.valuation.layer.revaluation"

    def action_validate_revaluation(self):
        res = super().action_validate_revaluation()
        self.product_id._apply_fifo_cost_rule(self.company_id)
        return res
