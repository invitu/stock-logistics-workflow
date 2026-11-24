# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Account FIFO Cost Rule",
    "summary": "Choose how the cost of FIFO products is computed",
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "Inventory/Inventory",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "author": "INVITU, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["stock_account"],
    "data": [
        "data/ir_default_data.xml",
        "views/product_category_views.xml",
    ],
}
