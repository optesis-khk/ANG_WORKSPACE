from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class TrimestrielLoyerWizard(models.TransientModel):
    _name = "trimestriel.loyer.wizard"
    _description = "report for Loyer Wizard"

    debut = fields.Date("Date debut")
    fin = fields.Date("Date fin")


class AnnuelLoyerWizard(models.TransientModel):
    _name = "annuel.loyer.wizard"
    _description = "report for annuel Wizard"

    debut = fields.Date("Date debut")
    fin = fields.Date("Date fin")
