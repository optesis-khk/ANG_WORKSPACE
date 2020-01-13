from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    honoraire_trim = fields.Boolean("Declaration honoraires trimestriel")
    loyer_trim = fields.Boolean("Declaration loyer trimestriel")
    honoraire_annuel = fields.Boolean("Declaration honoraires annuel")
    loyer_annuel = fields.Boolean("Declaration loyer annuel")
    nature = fields.Char("Nature")
    qualite = fields.Char("Qualite")

    @api.onchange("honoraire_trim","honoraire_annuel")
    def get_declaration_honoraire(self):
        for rec in self:
            if rec.honoraire_trim:
                rec.honoraire_annuel = True
                rec.loyer_trim = False
                rec.loyer_annuel = False
            if rec.honoraire_annuel:
                rec.loyer_trim = False
                rec.loyer_annuel = False

    @api.onchange("loyer_trim","loyer_annuel")
    def get_declaration_loyer(self):
        for rec in self:
            if rec.loyer_trim:
                rec.loyer_annuel = True
                rec.honoraire_trim = False
                rec.honoraire_annuel = False
            if rec.loyer_annuel:
                rec.honoraire_trim = False
                rec.honoraire_annuel = False

    @api.onchange("company_type")
    def get_declaration_type(self):
        for rec in self:
            if rec.company_type == 'company':
                rec.honoraire_trim = False
                rec.loyer_trim = False
