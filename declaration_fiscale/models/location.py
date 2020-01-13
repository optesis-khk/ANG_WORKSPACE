from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class OptesisImmeuble(models.Model):
    _name = "optesis.location"

    name = fields.Char('Référence')
    adresse = fields.Char("Adresse de l'immeuble loue")
    partner_id = fields.Many2one("res.partner", "Fournisseur")
    usage = fields.Selection(selection=[('habitayion', 'Habitation'), ('commercial', 'Commercial'), ('autre', 'Autres')], string="Usage")
    loyer = fields.Float("Loyer mensuel")
    debut = fields.Date("Debut contrat")
    fin = fields.Date("Fin contrat")

    @api.multi
    @api.constrains('fin', 'debut')
    def validate_date_range(self):
        for rec in self:
            if rec.fin < rec.debut:
                raise ValidationError(_("La date de fin doit etre supérieur a la date de début pour"))
        return True
