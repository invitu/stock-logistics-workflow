# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _create_in_svl(self, forced_quantity=None):
        # The core cost update runs before the incoming layer exists.
        layers = super()._create_in_svl(forced_quantity=forced_quantity)
        layers._apply_fifo_cost_rule()
        return layers

    def _create_out_svl(self, forced_quantity=None):
        layers = super()._create_out_svl(forced_quantity=forced_quantity)
        layers._apply_fifo_cost_rule()
        return layers
