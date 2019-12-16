from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class TrimestrielIndividualWizard(models.TransientModel):
    _name = "trimestriel.individual.wizard"
    _description = "report for individual Wizard"

    debut = fields.Date("Date debut")
    fin = fields.Date("Date fin")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    @api.multi
    def check_report(self):
        data = {}
        data['form'] = self.read(['debut', 'fin', 'company_id'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['debut', 'fin', 'company_id'])[0])
        #return self.env.ref('declaration_fiscale.report_trimestre_tier').report_action(self, data=data)
        return {'type': 'ir.actions.report','report_name': 'declaration_fiscale.report_trimestre_tier','report_type':"qweb-pdf",'data': data,}


class AnnuelIndividualWizard(models.TransientModel):
    _name = "annuel.individual.wizard"
    _description = "report for annuel Wizard"

    debut = fields.Date("Date debut")
    fin = fields.Date("Date fin")
