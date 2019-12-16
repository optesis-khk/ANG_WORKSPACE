import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError


class ReportDeclarationFiscale(models.AbstractModel):
    _name = 'report.declaration_fiscale.report_trimestre_tier'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        move_records = []
        partners = self.env['res.partner'].search([('supplier', '=', True), ('company_type', '=', 'person')])
        for partner in partners:
            self.env.cr.execute("SELECT p.name, p.street , sum(mv.debit), \
                            FROM res_partner as p, account_move_line as mv \
                            WHERE p.id = mv.partner_id = %s and sum(mv.debit) > 250000 \
                            AND mv.date_maturity <= %s AND mv.date_maturity >= %s\
                            GROUP BY p.mane",
                            (partner.id, docs.dabut, docs.fin))
            result = self.env.cr.fetchone()[0] or 0.0
            move_records.append(result);
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
