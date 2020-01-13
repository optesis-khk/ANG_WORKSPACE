from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class PeriodeFiscale(models.Model):
    _name = "optesis.period"

    name = fields.Char("Periode fiscale")
    debut = fields.Date("Date de debut")
    fin = fields.Date("Date de fin")
    code = fields.Char("Code")

    @api.multi
    @api.constrains('fin', 'debut')
    def validate_date_range(self):
        _logger.info('dans fonction')
        for rec in self:
            if rec.fin < rec.debut:
                _logger.info('ok')
                raise ValidationError(_("La date de fin doit etre supérieur a la date de début"))
        return True
