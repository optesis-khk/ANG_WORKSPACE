import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class ReportDeclarationFiscaleTrimTier(models.AbstractModel):
    _name = 'report.declaration_fiscale.report_trimestre_tier'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        lines = []
        self.env.cr.execute("select rp.name, rp.street, sum(ai.amount_untaxed) as amount_untaxed, sum(ai.amount_tax) as amount_tax, rp.vat\
                             from account_invoice as ai, res_partner as rp\
                             where ai.partner_id = rp.id and rp.supplier is true and rp.honoraire_trim is true and (ai.date between %s AND %s) and ai.amount_tax != 0\
                             group by rp.name, rp.street, rp.vat", (docs.exercice_id.debut, docs.exercice_id.fin))
        result = self.env.cr.dictfetchall()
        for line in result:
            lines.append(line);
        _logger.info('le resultat de la requete => %s',lines)
        docargs = {
           'doc_ids': self.ids,
           'doc_model': self.model,
           'docs': docs,
           'time': time,
           'lines': lines
        }
        return docargs


class ReportDeclarationFiscaleAnnTier(models.AbstractModel):
    _name = 'report.declaration_fiscale.report_annuel_tier'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        lines = []
        self.env.cr.execute("select rp.name, rp.street, rp.nature, rp.qualite, sum(ai.amount_untaxed) as amount_untaxed, rp.vat\
                             from account_invoice as ai, res_partner as rp\
                             where ai.partner_id = rp.id and rp.supplier is true and rp.honoraire_annuel is true and (ai.date between %s AND %s) and ai.amount_tax != 0 and amount_untaxed>300000\
                             group by rp.name, rp.street, rp.vat, rp.nature, rp.qualite", (docs.exercice_id.debut, docs.exercice_id.fin))
        result = self.env.cr.dictfetchall()
        for line in result:
            lines.append(line);
        _logger.info('le resultat de la requete => %s',lines)
        docargs = {
           'doc_ids': self.ids,
           'doc_model': self.model,
           'docs': docs,
           'time': time,
           'lines': lines
        }
        return docargs

class ReportDeclarationFiscaleTrimLoyer(models.AbstractModel):
    _name = 'report.declaration_fiscale.report_trimestre_loyer'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        lines = []
        self.env.cr.execute("select rp.name, ol.adresse, ol.usage, sum(ai.amount_untaxed) as loyer, sum(ai.amount_tax) as irpp\
                             from account_invoice as ai, res_partner as rp, optesis_location as ol\
                             where ai.partner_id = rp.id and ai.location_id = ol.id and rp.supplier is true and rp.loyer_trim is true and (ai.date between %s AND %s) and ai.amount_tax != 0\
                             group by rp.name, ol.adresse, ol.usage", (docs.exercice_id.debut, docs.exercice_id.fin))
        result = self.env.cr.dictfetchall()
        for line in result:
            lines.append(line);
        _logger.info('le resultat de la requete => %s',lines)
        docargs = {
           'doc_ids': self.ids,
           'doc_model': self.model,
           'docs': docs,
           'time': time,
           'lines': lines
        }
        return docargs


class ReportDeclarationFiscaleAnnLoyer(models.AbstractModel):
    _name = 'report.declaration_fiscale.report_annuel_loyer'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        lines = []
        self.env.cr.execute("select rp.name, ol.adresse, ol.usage, sum(ai.amount_untaxed) as loyer\
                             from account_invoice as ai, res_partner as rp, optesis_location as ol\
                             where ai.partner_id = rp.id and ai.location_id = ol.id and rp.supplier is true and rp.loyer_annuel is true and (ai.date between %s AND %s) and ai.amount_tax != 0 and loyer > 300000\
                             group by rp.name, ol.adresse, ol.usage", (docs.exercice_id.debut, docs.exercice_id.fin))
        result = self.env.cr.dictfetchall()
        for line in result:
            lines.append(line);
        _logger.info('le resultat de la requete => %s',lines)
        docargs = {
           'doc_ids': self.ids,
           'doc_model': self.model,
           'docs': docs,
           'time': time,
           'lines': lines
        }
        return docargs
