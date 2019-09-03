from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import float_compare

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    op_id = fields.Many2one("optesis.ordre.paiement", "Ordre de paiement")

    @api.onchange("op_id")
    def get_lines(self):
        if self.op_id:
            new_lines = self.env['account.invoice.line']
            for line in self.op_id.line_ids:
                new_lines += new_lines.new(line._prepare_invoice_line())
            self.partner_id = self.op_id.partner_id.id
            self.invoice_line_ids += new_lines
            self.op_id = False
            list = []
            for line in self.invoice_line_ids:
                list.append(line.origin.name)
            return {'domain':{'op_id':[('name','not in', list),('state', '=', 'validate')]}}
            return {}

    @api.multi
    def action_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: not inv.partner_id):
            raise UserError(_("The field Vendor is required, please complete it to validate the Vendor Bill."))
        if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
            raise UserError(_("Invoice must be in draft state in order to validate it."))
        if to_open_invoices.filtered(lambda inv: float_compare(inv.amount_total, 0.0, precision_rounding=inv.currency_id.rounding) == -1):
            raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
        if to_open_invoices.filtered(lambda inv: not inv.account_id):
            raise UserError(_('No account was found to create the invoice, be sure you have installed a chart of account.'))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        for op_line in self.invoice_line_ids:
            op_line.origin.state = "compta"
            for line in op_line.origin.line_ids:
                line.origin.bc_number.state = "compta"
        return to_open_invoices.invoice_validate()

    @api.multi
    def action_invoice_paid(self):
        # lots of duplicate calls to action_invoice_paid, so we remove those already paid
        to_pay_invoices = self.filtered(lambda inv: inv.state != 'paid')
        if to_pay_invoices.filtered(lambda inv: inv.state not in ('open', 'in_payment')):
            raise UserError(_('Invoice must be validated in order to set it to register payment.'))
        if to_pay_invoices.filtered(lambda inv: not inv.reconciled):
            raise UserError(_('You cannot pay an invoice which is partially paid. You need to reconcile payment entries first.'))

        for invoice in to_pay_invoices:
            if any([move.journal_id.post_at_bank_rec and move.state == 'draft' for move in invoice.payment_move_line_ids.mapped('move_id')]):
                invoice.write({'state': 'in_payment'})
            else:
                invoice.write({'state': 'paid'})
                for op_line in self.invoice_line_ids:
                    op_line.origin.state = "paye"
                    for line in op_line.origin.line_ids:
                        line.origin.bc_number.state = "paye"




class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    origin = fields.Many2one("optesis.ordre.paiement", string='Origine')
