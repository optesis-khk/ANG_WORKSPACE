from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class OrdrePaiement(models.Model):
    _name = "optesis.ordre.paiement"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char("Ordre de paiement", readonly="True")
    state = fields.Selection([
            ('draft','Brouillon'),
            ('confirm', 'Confirmé'),
            ('validate', 'Validé'),
            ('cancel','Annuler'),
            ('compta', 'Comptabilisé'),
            ('paye', 'Payé')
        ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
             " * The 'In Payment' status is used when payments have been registered for the entirety of the invoice in a journal configured to post entries at bank reconciliation only, and some of them haven't been reconciled with a bank statement line yet.\n"
             " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")


    partner_id = fields.Many2one('res.partner', string='Fournisseur', change_default=True,
        readonly=True, states={'draft': [('readonly', False)]},
        track_visibility='always', required=True)

    date = fields.Date(string='Date ordre de paiement',
        readonly=True, states={'draft': [('readonly', False)]}, index=True,
        help="Keep empty to use the current date", copy=False)

    reference = fields.Char(string='Reference fournisseur.', copy=False, readonly=True, states={'draft': [('readonly', False)]},
        help='The payment communication that will be automatically populated once the invoice validation. You can also write a free communication.')

    date_due = fields.Date(string="Date d'echeance",
        readonly=True, states={'draft': [('readonly', False)]}, index=True, copy=False,
        help="If you use payment terms, the due date will be computed automatically at the generation "
             "of accounting entries. The Payment terms may compute several due dates, for example 50% "
             "now and 50% in one month, but if you want to force a due date, make sure that the payment "
             "term is not set on the invoice. If you keep the Payment terms and the due date empty, it "
             "means direct payment.")

    vendor_bill_id = fields.Many2one('stock.picking', string="Bon d'entrer")

    partner_bank_id = fields.Many2one('res.partner.bank', string='Bank Account',
        help='Bank Account Number to which the invoice will be paid. A Company bank account if this is a Customer Invoice or Vendor Credit Note, otherwise a Partner bank account number.',
        readonly=True, states={'draft': [('readonly', False)]})

    line_ids = fields.One2many("optesis.ordre_paiement.line", "op_id", string="Lignes")

    infos_lines = fields.One2many("optesis.infos.line", "op_id", string="Lignes d'informations")

    currency_id = fields.Many2one('res.currency', string='Currency',  default=lambda self: self.env.user.company_id.currency_id)

    amount_untaxed = fields.Monetary(string='Montant HT', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')


    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
    }

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('optesis.ordre.paiement') or '/'
        result = super(OrdrePaiement, self).create(vals)
        return result

    @api.depends('line_ids.price_subtotal')
    def _amount_all(self):
        for op in self:
            amount_untaxed = amount_tax = 0.0
            for line in op.line_ids:
                amount_untaxed += line.price_subtotal
                amount_tax += (line.quantity * line.price_unit * line.taxes_id.amount) / 100
            op.update({
                'amount_untaxed': op.currency_id.round(amount_untaxed),
                'amount_tax': op.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })


    @api.onchange("vendor_bill_id")
    def get_lines(self):
        list = []
        if self.vendor_bill_id:
            new_lines = self.env['optesis.ordre_paiement.line']
            for line in self.vendor_bill_id.move_ids_without_package:
                new_lines += new_lines.new(line._prepare_line())
            self.line_ids += new_lines
            self.partner_id = self.vendor_bill_id.partner_id.id
            self.vendor_bill_id = False
            for line in self.line_ids:
                list.append(line.origin.name)
            return {'domain':{'vendor_bill_id':[('name','not in', list), ('state', 'in', ('done', 'immo')), ('op', '=', False), ('picking_type_id.default_location_dest_id', '!=', False)]}}

    @api.onchange("line_ids")
    def get_infos_lines(self):
        infos_lines = []
        for line in self.line_ids:
            if line.origin:
                infos_lines.append((0,0,{"bc_number":line.origin.bc_number.id, "be_number":line.origin.name}))
        self.infos_lines = infos_lines

    @api.multi
    def button_confirm(self):
        for record in self:
            record.state = "confirm"

    @api.multi
    def button_valide(self):
        for record in self:
            record.state = "validate"
            for line in record.line_ids:
                line.origin.op = True
                line.origin.bc_number.state = "liquide"

    @api.multi
    def button_cancel(self):
        for record in self:
            record.state = "cancel"

    @api.multi
    def button_draft(self):
        for record in self:
            record.state = "draft"

    @api.multi
    def unlink(self):
        if self.filtered(lambda x: x.state in ('validate', 'cancel')):
            raise UserError(_('Cet enregistrement ne peux etre supprime'))
        return super(OrdrePaiement, self).unlink()


class OrdrePaiementLine(models.Model):
    _name = "optesis.ordre_paiement.line"

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Article', ondelete='restrict', index=True)
    account_id = fields.Many2one('account.account', string='Compte', domain=[('deprecated', '=', False)],  help="The income or expense account related to the selected product.")
    quantity = fields.Float(string='Quantite', required=True, default=1)
    account_analytic_id = fields.Many2one('account.analytic.account',
                                          'Analytic Account',
                                          track_visibility='onchange')
    price_unit = fields.Float(string='Prix unitaire', required=True)
    taxes_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Sous total', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency',  default=lambda self: self.env.user.company_id.currency_id)
    origin = fields.Many2one("stock.picking")
    op_id = fields.Many2one("optesis.ordre.paiement", ondelete="cascade")

    @api.depends('quantity', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])
            line.update({'price_subtotal': taxes['total_excluded']})

    def _prepare_compute_all_values(self):
        self.ensure_one()
        return {
            'price_unit': self.price_unit,
            'currency_id': self.currency_id,
            'product_qty': self.quantity,
            'product': self.product_id,
            'partner': self.op_id.partner_id,
        }

    @api.onchange("product_id")
    def onchange_product(self):
        for line in self:
            if line.product_id:
                line.name = line.product_id.name
                line.account_id = line.product_id.categ_id.property_account_expense_categ_id or line.product_id.property_account_expense_id

    def _prepare_invoice_line(self):
        data = {
            'name': self.name,
            'origin': self.op_id.id,
            'uom_id': self.product_id.id,
            'product_id': self.product_id.id,
            'account_id': self.account_id.id,
            'price_unit': self.price_unit,
            'account_analytic_id': self.account_analytic_id.id,
            'quantity': self.quantity,
            'invoice_line_tax_ids': self.taxes_id
        }
        return data


class OptesisInfoLine(models.Model):
    _name = "optesis.infos.line"

    name = fields.Char("Designation", related="op_id.name")
    bc_number = fields.Many2one('purchase.order', string='Numero de bon de commande')
    pvr_number = fields.Char(string='Numéro de PVR')
    be_number = fields.Char(string="Numéro de bon d'entrer")
    op_id = fields.Many2one("optesis.ordre.paiement", ondelete="cascade")
