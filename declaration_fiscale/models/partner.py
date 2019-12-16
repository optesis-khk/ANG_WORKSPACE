from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    honoraire = fields.Boolean("Declaration honoraires")
    loyer = fields.Boolean("Declaration loyer")
