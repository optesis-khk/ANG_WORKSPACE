# -*- coding: utf-8 -*-
###################################################################################
#    A part of OpenHRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Treesa Maria Jude (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################


from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class BonusRuleInput(models.Model):
    _inherit = 'hr.payslip'

    net_salary = fields.Float(string="Net Salary")

    def get_inputs(self, contract_ids, date_from, date_to):
        res = super(BonusRuleInput, self).get_inputs(contract_ids, date_from, date_to)
        net_salary_line = {
            'name': "Net Salary",
            'code': 'NET',
            'contract_id': contract_ids[0].id if contract_ids else False,
            'amount': self.net_salary,

        }
        res += [net_salary_line]
        return res
