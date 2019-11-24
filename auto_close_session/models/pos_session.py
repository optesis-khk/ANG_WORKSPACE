from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)

class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def auto_close_session(self):
        server_dt = DF
        _logger.info("entrer dans fonction autoclose")
        pos_session = self.env['pos.session']
        sessions = pos_session.search([('id', '=', 6)])
        for session in sessions:
            _logger.info(session.start_at)
            if fields.Datetime.now() > (session.start_at + timedelta(hours=12)):
                _logger.info('the close function is called ')
                session.action_pos_session_closing_control()
