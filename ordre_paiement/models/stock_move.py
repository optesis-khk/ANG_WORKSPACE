from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools.float_utils import float_compare, float_round, float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"

    prix_achat = fields.Float("Prix d'achat")

    def _prepare_line(self):
        data = {
            'product_id': self.product_id.id,
            'name': self.product_id.name,
            'account_id': self.product_id.categ_id.property_account_expense_categ_id.id or self.product_id.property_account_expense_id.id,
            'account_analytic_id': self.analytic_account_id.id,
            'quantity': self.product_uom_qty,
            'price_unit': self.prix_achat,
            'origin': self.picking_id.id,
        }
        return data

    # @api.one
    # def op_create(self):
    #     lines = []
    #     for line in self.picking_id.move_ids_without_package:
    #         values = line._prepare_line()
    #         lines.append((0, 0, values))
    #
    #     data = {
    #         'partner_id': self.picking_id.partner_id.id,
    #         'date': self.picking_id.date,
    #         'origin': self.picking_id.name,
    #         'bc_number':self.picking_id.origin,
    #         'be_number':self.picking_id.name,
    #         'line_ids': lines,
    #     }
    #
    #     self.env["optesis.ordre.paiement"].create(data)
    #     return True
