# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    amount_total_to_word = fields.Char(compute='_compute_amount_total_to_word', store=True)

    to_19_fr = (u'zĂŠro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six',
                'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize',
                'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf')
    tens_fr = (
        'vingt', 'trente', 'quarante', 'Cinquante', 'Soixante', 'Soixante-dix', 'Quatre-vingts', 'Quatre-vingt Dix')

    denom_fr = ('',
                'Mille', 'Millions', 'Milliards', 'Billions', 'Quadrillions',
                'Quintillion', 'Sextillion', 'Septillion', 'Octillion', 'Nonillion',
                'DĂŠcillion', 'Undecillion', 'Duodecillion', 'Tredecillion', 'Quattuordecillion',
                'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Icosillion', 'Vigintillion')

    def _convert_nn_fr(self, val):
        """ convert a value < 100 to French
        """
        if val < 20:
            return self.to_19_fr[val]
        for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(self.tens_fr)):
            if dval + 10 > val:
                if val % 10:
                    return dcap + '-' + self.to_19_fr[val % 10]
                return dcap

    def _convert_nnn_fr(self, val):
        """ convert a value < 1000 to french

            special cased because it is the level that kicks
            off the < 100 special case.  The rest are more general.  This also allows you to
            get strings in the form of 'forty-five hundred' if called directly.
        """
        word = ''
        (mod, rem) = (val % 100, val // 100)
        if rem > 0:
            word = self.to_19_fr[rem] + ' Cent'
            if mod > 0:
                word += ' '
        if mod > 0:
            word += self._convert_nn_fr(mod)
        return word

    def french_number(self, val):
        if val < 100:
            return self._convert_nn_fr(val)
        if val < 1000:
            return self._convert_nnn_fr(val)
        for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(self.denom_fr))):
            if dval > val:
                mod = 1000 ** didx
                l = val // mod
                r = val - (l * mod)
                ret = self._convert_nnn_fr(l) + ' ' + self.denom_fr[didx]
                if r > 0:
                    ret = ret + ', ' + self.french_number(r)
                return ret


    def amount_to_text_fr(self, number, currency):
        number = '%.2f' % number
        units_name = currency
        list = str(number).split('.')
        start_word = self.french_number(abs(int(list[0])))
        end_word = self.french_number(int(list[1]))
        cents_number = int(list[1])
        cents_name = (cents_number > 1) and ' Cents' or ' Cent'
        final_result = start_word + ' ' + units_name + ' ' + end_word + ' ' + cents_name
        return final_result

    @api.multi
    @api.depends('amount_total')
    def _compute_amount_total_to_word(self):
        _logger.info('dans la function compute')
        for record in self:
            record.amount_total_to_word = record.amount_to_text_fr(record.amount_total, currency='')[:-10]
