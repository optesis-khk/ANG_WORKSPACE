from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class OptesisImmeuble(models.Model):
    _name = "optesis.immeuble"

    name = fields.Char('Adresse')
