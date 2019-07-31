from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, exceptions, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError, ValidationError, Warning
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import odoo.addons.decimal_precision as dp
from odoo.tools import ustr

from odoo.tools.amount_to_text import amount_to_text_fr



class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    crossovered_budget_line = fields.One2many('crossovered.budget.lines', 'analytic_account_id','Budgets', compute='_get_lines')
    amount_total_to_word = fields.Char(compute='_compute_amount_total_to_word', store=True)

    @api.multi
    @api.depends('amount_total')
    def _compute_amount_total_to_word(self):
        self.amount_total_to_word = amount_to_text_fr(self.amount_total, currency='')[:-10]


    @api.multi
    @api.depends('order_line')
    def _get_lines(self):
        temoin = []
        for line in self.order_line:
            budgets = self.env['crossovered.budget.lines'].search([('analytic_account_id','=',line.account_analytic_id.id),('general_budget_id.account_ids','=',line.account_id.id)])
            if budgets:
                for budget in budgets:
                    if budget.id not in temoin:
                        #_logger.info("budget_id => %s , temoin => %s",budget.id, temoin)
                        self.crossovered_budget_line += budget
                        temoin.append(budget.id)

    @api.depends('state')
    def _set_purchase_user(self):
        for rec in self:
            if rec.state == 'draft' or 'sent':
                rec.purchase_user_id = self.env.user.id,

    @api.model
    def _get_finance_validation_amount(self):
#         finance_validation_amount = self.env['ir.values'].get_default('purchase.config.settings', 'finance_validation_amount')
        finance_validation_amount = self.env.user.company_id.finance_validation_amount
        return finance_validation_amount

    @api.model
    def _get_director_validation_amount(self):
#         director_validation_amount = self.env['ir.values'].get_default('purchase.config.settings', 'director_validation_amount')
        director_validation_amount = self.env.user.company_id.director_validation_amount
        return director_validation_amount

    @api.model
    def _get_three_step_validation(self):
#         three_step_validation = self.env['ir.values'].get_default('purchase.config.settings', 'three_step_validation')
        three_step_validation = self.env.user.company_id.three_step_validation
        return three_step_validation

    @api.model
    def _get_email_template_id(self):
#         email_template_id = self.env['ir.values'].get_default('purchase.config.settings', 'email_template_id')
        email_template_id = self.env.user.company_id.email_template_id
        return email_template_id

    @api.model
    def _get_refuse_template_id(self):
#         refuse_template_id = self.env['ir.values'].get_default('purchase.config.settings', 'refuse_template_id')
        refuse_template_id = self.env.user.company_id.refuse_template_id
        return refuse_template_id

    state = fields.Selection(selection_add=[
        ('finance_approval', 'Waiting Finance Approval'),
        ('director_approval', 'Waiting Director Approval'),
        ('refuse', 'Refuse')],
        string='Status',
    )
    po_refuse_user_id = fields.Many2one(
        'res.users',
        string="Refused By",
        readonly = True,
    )
    po_refuse_date = fields.Date(
        string="Refused Date",
        readonly=True
    )
    refuse_reason_note = fields.Text(
        string="Refuse Reason",
        readonly=True
    )
    dept_manager_id = fields.Many2one(
        'res.users',
        string='Purchase/Department Manager',
        states={'done':[('readonly',True)], 'cancel':[('readonly',True)]}
    )
    finance_manager_id = fields.Many2one(
        'res.users',
        string='Finance Manager',
        states={'done':[('readonly',True)], 'cancel':[('readonly',True)]}
    )
    director_manager_id = fields.Many2one(
        'res.users',
        string='Director Manager',
        states={'done':[('readonly',True)], 'cancel':[('readonly',True)]}
    )
    approve_dept_manager_id = fields.Many2one(
        'res.users',
        string='Approve Department Manager',
        readonly=True,
    )
    approve_finance_manager_id = fields.Many2one(
        'res.users',
        string='Approve Finance Manager',
        readonly=True,
    )
    approve_director_manager_id = fields.Many2one(
        'res.users',
        string='Approve Director Manager',
        readonly=True,
    )
    dept_manager_approve_date = fields.Datetime(
        string='Department Manager Approve Date',
        readonly=True,
    )
    finance_manager_approve_date = fields.Datetime(
        string='Finance Manager Approve Date',
        readonly=True,
    )
    director_manager_approve_date = fields.Datetime(
        string='Director Manager Approve Date',
        readonly=True,
    )
    purchase_user_id = fields.Many2one(
        'res.users',
        string='Purchase User',
        compute='_set_purchase_user',
        store=True,
    )


    @api.multi
    def _write(self, vals):
        for order in self:
            amount_total = order.currency_id.compute(order.amount_total, order.company_id.currency_id)
            finance_validation_amount = self._get_finance_validation_amount()
            po_double_validation_amount = self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id)
            if vals.get('state') == 'to approve':
                if not order.dept_manager_id:
                    raise UserError(_('Please select Purchase/Department Manager.'))
                else:
                    email_to = order.dept_manager_id.email
                    email_template_id = self._get_email_template_id()
                    print('ddddddddddddddd==============================',email_to,email_template_id)
                    ctx = self._context.copy()
                    print('ctx===================================',ctx)
                    ctx.update({'name': order.dept_manager_id.name})
                    print('ffffffff==============================',ctx)
                    #reminder_mail_template.with_context(ctx).send_mail(user)
                    if email_template_id:
                        print('[[[[[[[[[[[[[[[===================]]]',email_template_id)
                        email_template_id.with_context(ctx).send_mail(self.id, email_values={'email_to': email_to, 'subject': _('Purchase Order: ') + order.name + _(' (Approval Waiting)')})
                        print('=====================email_template_id====================')

            if vals.get('state') == 'finance_approval':
                if not order.finance_manager_id:
                    raise UserError(_('Please select Finance Manager.'))
                else:
                    email_to = order.finance_manager_id.email
                    email_template_id = self._get_email_template_id()
#                     mail = self.env['mail.template'].browse(email_template_id)
                    ctx = self._context.copy()
                    ctx.update({'name': order.finance_manager_id.name})
                    #mail.send_mail(self.id, email_values={'email_to': email_to, 'subject': "Finance Manager Approve"})
                    if email_template_id:
                        email_template_id.with_context(ctx).send_mail(self.id, email_values={'email_to': email_to, 'subject': _('Purchase Order: ') + order.name + _(' (Approval Waiting)')})

            if vals.get('state') == 'director_approval':
                if not order.director_manager_id:
                    raise UserError(_('Please select Director Manager.'))
                else:
                    email_to = order.director_manager_id.email
                    email_template_id = self._get_email_template_id()
#                     mail = self.env['mail.template'].browse(email_template_id)
                    ctx = self._context.copy()
                    ctx.update({'name': order.director_manager_id.name})
                    #mail.send_mail(self.id, email_values={'email_to': email_to, 'subject': "Director Manager Approve"})
                    if email_template_id:
                        email_template_id.with_context(ctx).send_mail(self.id, email_values={'email_to': email_to, 'subject': _('Purchase Order: ') + order.name + _(' (Approval Waiting)')})

            if order.state == 'to approve' and vals.get('state') == 'purchase':
                order.approve_dept_manager_id = self.env.user.id
                order.dept_manager_approve_date = fields.Datetime.now()
            elif order.state == 'to approve' and vals.get('state') == 'finance_approval':
                order.approve_dept_manager_id = self.env.user.id
                order.dept_manager_approve_date = fields.Datetime.now()

            if order.state == 'finance_approval' and vals.get('state') == 'purchase':
                order.approve_finance_manager_id = self.env.user.id
                order.finance_manager_approve_date = fields.Datetime.now()
            elif order.state == 'finance_approval' and vals.get('state') == 'director_approval':
                order.approve_finance_manager_id = self.env.user.id
                order.finance_manager_approve_date = fields.Datetime.now()

            if order.state == 'director_approval' and vals.get('state') == 'purchase':
                order.approve_director_manager_id = self.env.user.id
                order.director_manager_approve_date = fields.Datetime.now()
        return super(PurchaseOrder, self)._write(vals)


    @api.multi
    def button_finance_approval(self):
        finance_validation_amount = self._get_finance_validation_amount()
        director_validation_amount = self._get_director_validation_amount()
        amount_total = self.currency_id.compute(self.amount_total, self.company_id.currency_id)
        for order in self:
            if amount_total > director_validation_amount:
                order.write({'state': 'director_approval'})
            if amount_total < director_validation_amount:
                order.button_director_approval()
        return True

    @api.multi
    def button_director_approval(self):
        for order in self:
            order.with_context(call_super=True).button_approve()
        return True

    @api.multi
    def button_approve(self, force=False):
        for line in self.order_line:
            if line.price_subtotal and line.available:
                ok = line.available - line.price_subtotal
                if ok < 0 or line.available == 0 :
                    raise Warning('Attention votre budget est insusffisant vour effectuer l\'achat')
        if self._context.get('call_super', False):
            if self.crossovered_budget_line:
                for crossovered_line in self.crossovered_budget_line:
                    self.order_line.create_budget_lines(crossovered_line.general_budget_id.id, crossovered_line.analytic_account_id)
            return super(PurchaseOrder, self).button_approve()

        three_step_validation = self._get_three_step_validation()
        if not three_step_validation:
            if self.crossovered_budget_line:
                for crossovered_line in self.crossovered_budget_line:
                    self.order_line.create_budget_lines(crossovered_line.general_budget_id.id, crossovered_line.analytic_account_id)
            return super(PurchaseOrder, self).button_approve()

        amount_total = self.currency_id.compute(self.amount_total, self.company_id.currency_id)
        po_double_validation_amount = self.env.user.company_id.currency_id.compute(self.company_id.po_double_validation_amount, self.currency_id)
        finance_validation_amount = self._get_finance_validation_amount()
        director_validation_amount = self._get_director_validation_amount()
#         if finance_validation_amount > amount_total:
#             return super(PurchaseOrder, self).button_approve()

        if three_step_validation and not self._context.get('call_super', False):
             for order in self:
                if amount_total > po_double_validation_amount and order.state != 'to approve':
                    order.write({'state': 'to approve'})
                elif amount_total < finance_validation_amount and order.state == 'to approve':
                    if self.crossovered_budget_line:
                        for crossovered_line in self.crossovered_budget_line:
                            self.order_line.create_budget_lines(crossovered_line.general_budget_id.id, crossovered_line.analytic_account_id)
                    return super(PurchaseOrder, self).button_approve()
                elif order.state == 'to approve':
                    order.state = 'finance_approval'
                else:
                    return super(PurchaseOrder, self).button_approve()

#                 if order.state == 'to approve':
#                     order.state = 'finance_approval'
        if self.crossovered_budget_line:
                for crossovered_line in self.crossovered_budget_line:
                    self.order_line.create_budget_lines(crossovered_line.general_budget_id.id, crossovered_line.analytic_account_id)
        return True

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    account_id = fields.Many2one('account.account', string='Compte',
        required=True, domain=[('deprecated', '=', False)],
        help="The income or expense account related to the selected product.")

    available =  fields.Float(string='Montant budget restant',compute="_get_available", digits=0 , default="0")

    planned =  fields.Float(string='Montant budget prevu',compute="_get_planned", digits=0 , default="0")

    analytic_budget_ids = fields.One2many('account.budget.line', 'move_id', string='Account Budget lines')

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.price_unit = self.product_qty = 0.0
        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        self.account_id = self.product_id.property_account_expense_id.id or self.product_id.categ_id.property_account_expense_categ_id.id
        result['domain'] = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}

        product_lang = self.product_id.with_context({
            'lang': self.partner_id.lang,
            'partner_id': self.partner_id.id,
        })
        self.name = product_lang.display_name
        if product_lang.description_purchase:
            self.name += '\n' + product_lang.description_purchase

        fpos = self.order_id.fiscal_position_id
        if self.env.uid == SUPERUSER_ID:
            company_id = self.env.user.company_id.id
            self.taxes_id = fpos.map_tax(self.product_id.supplier_taxes_id.filtered(lambda r: r.company_id.id == company_id))
        else:
            self.taxes_id = fpos.map_tax(self.product_id.supplier_taxes_id)

        self._suggest_quantity()
        self._onchange_quantity()

        return result

    @api.multi
    @api.depends('account_id','account_analytic_id')
    def _get_available(self):
        for record in self:
            if record.account_id and record.account_analytic_id:
                for line in record.account_analytic_id.crossovered_budget_line:
                    if record.account_id.id in line.general_budget_id.account_ids.ids:
                        record.available = line.available_amount
                        break

    @api.multi
    @api.depends('account_id','account_analytic_id')
    def _get_planned(self):
        for record in self:
            if record.account_id and record.account_analytic_id:
                for line in record.account_analytic_id.crossovered_budget_line:
                    if record.account_id.id in line.general_budget_id.account_ids.ids:
                        record.planned = line.planned_amount
                        break


    @api.onchange('price_subtotal','available')
    def _budget_control(self):
        if self.price_subtotal and self.available:
            ok = self.available - self.price_subtotal
            if ok < 0 or self.available == 0:
                raise Warning('Attention votre budget est insusffisant vour effectuer l\'achat')


    @api.multi
    def create_budget_lines(self, general_budget_id, analytic_account_id):
        """ Create analytic items upon validation of an account.move.line having an budget account. This
            method first remove any existing analytic item related to the line before creating any new one.
        """
        for obj_line in self:
            if obj_line.account_analytic_id == analytic_account_id:
                vals_line = obj_line._prepare_budget_line(general_budget_id)[0]
                self.env['account.budget.line'].create(vals_line)

    @api.one
    def _prepare_budget_line(self, general_budget_id):
        """ Prepare the values used to create() an account.budget.line upon validation of an purchase.order.line having
            an analytic account. This method is intended to be extended in other modules.
        """
        return {
            'name': self.name,
            'date': self.date_planned,
            'account_id': self.account_analytic_id.id or False,
            'unit_amount': self.product_qty,
            'product_id': self.product_id.id or False,
            'amount': self.price_subtotal,
            'available_amount':self.available,
            'planned_amount':self.planned,
            'general_budget_id':general_budget_id or False,
            'general_account_id': self.account_id.id or False,
            'ref': self.order_id.name,
            'partner_id':self.order_id.partner_id.id,
        }
