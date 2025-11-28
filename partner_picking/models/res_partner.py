# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    stock_picking_count = fields.Integer(
        string="Stock Pickings", compute="_compute_stock_picking_count"
    )

    def _compute_stock_picking_count(self):
        for partner in self:
            partner.stock_picking_count = self.env["stock.picking"].search_count(
                [
                    ("partner_id", "child_of", partner.id),
                    ("state", "not in", ("cancel", "draft")),
                ]
            )
