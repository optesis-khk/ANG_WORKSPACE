from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    location_id = fields.Many2one("optesis.location", string="Contrat de location")
    hide = fields.Boolean(string='Hide', compute="_compute_hide")

    @api.depends('partner_id')
    def _compute_hide(self):
        if self.partner_id.loyer_annuel is True:
             self.hide = True
        else:
             self.hide = False

    @api.multi
    @api.onchange("invoice_line_ids")
    def _get_price_unit(self):
        for line in self.invoice_line_ids:
            if self.location_id:
                line.price_unit = self.location_id.loyer
