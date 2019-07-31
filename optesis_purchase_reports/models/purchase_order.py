# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from num2words import num2words


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    amount_text = fields.Char('Montant en lettres', compute='get_amount_text')

    @api.one
    @api.depends('amount_total', 'currency_id')
    def get_amount_text(self):
        number_in_word = num2words(self.amount_total, lang='fr')
        self.amount_text = number_in_word and number_in_word.capitalize()

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: