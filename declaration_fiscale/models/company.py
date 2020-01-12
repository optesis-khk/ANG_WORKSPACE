from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.exceptions import ValidationError
import time

class Company(models.Model):
    _name = "res.company"
    _inherit = 'res.company'

    sigle = fields.Char("Sigle de la societe")
    forme = fields.Char("Forme")
    profession = fields.Char("Profession")
    lc = fields.Char("LC")
    nom_comptable = fields.Many2one("res.partner", "Nom du comptable")
    bp_comptable = fields.Char("BP du comptable")
    tel_comptable = fields.Char("Tel du comptable")

    @api.onchange("nom_comptable")
    def onchanhe_nomcomptable(self):
        if self.nom_comptable:
            self.bp_comptable = self.nom_comptable.zip
            self.tel_comptable = self.nom_comptable.phone
