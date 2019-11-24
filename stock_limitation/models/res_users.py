# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_users(models.Model):
    _inherit = 'res.users'

    @api.multi
    def _inverse_location_ids(self):
        """
        Inverse method for location_ids

        Methods:
         * _compute_user_ids of stock.location
        """
        self = self.sudo()
        for user in self:
            for loc in user.location_ids:
                loc._compute_user_ids()


    location_ids = fields.Many2many(
        'stock.location',
        'res_users_stock_location_own_rel_table',
        'stock_location_own_id',
        'res_users_own_id',
        'Available Locations',
        inverse=_inverse_location_ids,
        help="""
            User would have an access to that locations and all their child location
        """
    )
