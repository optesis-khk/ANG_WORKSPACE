from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
import time

class Company(models.Model):
    _name = "res.company"
    _inherit = 'res.company'

    sigle = fields.Char("Sigle de la societe")
    forme = fields.Char("Forme")
    profession = fields.Char("Profession")
    nom_comptable = fields.Many2one("res.partner", "Nom du comptable")
    bp_comptable = fields.Char("BP du comptable")
    tel_comptable = fields.Char("Tel du comptable")
    debut_ex = fields.Date("Date debut exerccice", default=time.strftime('%Y-01-01'))
    fin_ex = fields.Date("Date fin exerccice", default=time.strftime('%Y-12-31'))
    loyer_ids = fields.One2many("optesis.titre.loyer", "company_id", string="Titre de loyers")


    @api.onchange("nom_comptable")
    def onchanhe_nomcomptable(self):
        if self.nom_comptable:
            self.bp_comptable = self.nom_comptable.zip
            self.tel_comptable = self.nom_comptable.phone


class TitreLoyer(models.Model):
    _name = "optesis.titre.loyer"

    adresse = fields.Char("Adresse de l'immeuble loue")
    partner_id = fields.Many2one("res.partner", "Fournisseur")
    usage = fields.Selection(selection=[('habitayion', 'Habitation'), ('commercial', 'Commercial'), ('autre', 'Autres')], string="Usage")
    loyer = fields.Float("Loyer mensuel")
    irpp = fields.Float("IRPP retenu", compute="get_irpp", store="True")
    debut_c = fields.Date("Debut contrat")
    fin_c = fields.Date("Debut contrat")
    company_id = fields.Many2one("res.company")

    @api.depends("loyer")
    def get_irpp(self):
        if self.loyer:
            self.irpp = (self.loyer * 5) / 100
            return self.irpp
