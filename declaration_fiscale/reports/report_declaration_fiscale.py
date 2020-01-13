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
        # self.env.cr.execute("select otl.adresse, rp.name, otl.usage, sum(otl.loyer) as loyer, sum(otl.irpp) as irpp\
        #                      from optesis_titre_loyer as otl, res_partner as rp\
        #                      where otl.partner_id = rp.id and (otl.debut_c between %s AND %s) and (otl.fin_c between %s AND %s)\
        #                      group by otl.adresse, rp.name, otl.usage", (docs.exercice_id.debut, docs.exercice_id.fin, docs.exercice_id.debut, docs.exercice_id.fin))
        # result = self.env.cr.dictfetchall()
        # for line in result:
        #     lines.append(line);
        # _logger.info('le resultat de la requete => %s',lines)
        docargs = {
           'doc_ids': self.ids,
           'doc_model': self.model,
           'docs': docs,
           'time': time,
           #'lines': lines
        }
        return docargs


class ReportDeclarationFiscaleAnnLoyer(models.AbstractModel):
    _name = 'report.declaration_fiscale.report_annuel_loyer'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        move_records = []
        partners = self.env['res.partner'].search([('supplier', '=', True), ('company_type', '=', 'person')])
        # for partner in partners:
        #     self.env.cr.execute("SELECT p.name, p.street , sum(mv.debit), \
        #                     FROM res_partner as p, account_move_line as mv \
        #                     WHERE p.id = mv.partner_id = %s and sum(mv.debit) > 250000 \
        #                     AND mv.date_maturity <= %s AND mv.date_maturity >= %s\
        #                     GROUP BY p.mane",
        #                     (partner.id, docs.debut, docs.fin))
        #     result = self.env.cr.fetchone()[0] or 0.0
        #     move_records.append(result);
        # if docs.date_from and docs.date_to:
        #    for order in orders:
        #      if parse(docs.date_from) <= parse(order.date_order) and parse(docs.date_to) >= parse(order.date_order):
        #          sales_records.append(order);
        #      else:
        #          raise UserError("Please enter duration")

        docargs = {
           'doc_ids': self.ids,
           'doc_model': self.model,
           'docs': docs,
           'time': time,
           #'orders': sales_records
        }
        return docargs
