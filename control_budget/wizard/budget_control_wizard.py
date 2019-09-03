from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class BudgetControl(models.TransientModel):
    _name = 'budget.control.wizard'
    _description = 'Control budgetaire'

    purchase_id = fields.Many2one('purchase.order')

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        self.purchase_id.state = "done"
