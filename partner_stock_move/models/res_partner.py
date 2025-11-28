# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    stock_move_count = fields.Integer(
        string="Stock Moves", compute="_compute_stock_move_count"
    )

    def _compute_stock_move_count(self):
        for partner in self:
            partner.stock_move_count = self.env["stock.move"].search_count(
                [
                    ("picking_id.partner_id", "child_of", partner.id),
                    ("state", "not in", ("cancel", "draft")),
                ]
            )
