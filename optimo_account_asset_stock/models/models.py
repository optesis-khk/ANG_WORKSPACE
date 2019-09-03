  #-*- coding:utf-8 -*-
from odoo import models, fields, api, osv
from odoo.exceptions import ValidationError
import datetime
import time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_round, float_is_zero

import logging
_logger = logging.getLogger(__name__)


class Direction(models.Model):
    _name = "optesis.direction"
    _description = "optesis direction"
    _sql_constraints = [('name_unique', 'unique(name)', "Cette direction existe déja")]

    name = fields.Char(String="direction", required=True, size=50)
    description = fields.Char(String="description")


# class department(models.Model):
#     _name = "optesis.department"
#     _description = "optesis departement"
#     _sql_constraints = [('name_unique', 'unique(name)', "Ce département existe déja")]
#
#     name = fields.Char(String="Département", required=True, size=50)
#     description = fields.Char(String="description")
#     direction_id = fields.Many2one(comodel_name="optesis.direction", string="Direction", required=True)

class Service(models.Model):
    _name = "optesis.service"
    _description = "optesis service"
    _sql_constraints = [('name_unique', 'unique(name)', "Ce service existe déja")]

    name = fields.Char(String="Service", required=True, size=50)
    description = fields.Char(String="description")
    direction_id = fields.Many2one(comodel_name="optesis.direction", string="Direction", required=True)



class Agent(models.Model):
    _name = "optesis.agent"
    _description = "user database"

    name = fields.Char(string="Nom et Prénom",required="True", size=100)
    service = fields.Many2one(comodel_name="optesis.service", string="Service", required=True)

    # class Site(models.Model):
    #     _name = "optesis.site"
    #     _description = "optesis site"
    #     _sql_constraints = [('name_unique', 'unique(name)', "ce site existe déja")]
    #
    #     name = fields.Char(String="Site", required=True, size=50)
    #     address = fields.Char(String="Addresse")
    #     region = fields.Char(String="Région")
    #     locality = fields.Char(String="Localité")
    #     description = fields.Char(String="description")


class Building(models.Model):
    _name = "optesis.building"
    _description = "optesis building"

    name = fields.Char(String="Bâtiment", required=True, size=50)
    description = fields.Char(String="description")
    # site_id = fields.Many2one(comodel_name="optesis.site", string="Site", required=True)

class Level(models.Model):
    _name = "optesis.level"
    _description = "optesis level"

    name = fields.Char(String="Niveau", required=True, size=50)
    description = fields.Char(String="description")
    building_id = fields.Many2one(comodel_name="optesis.building", string="Bâtiment", required=True)
    # site_level = fields.Many2one(comodel_name="optesis.site", string="Site", required=True)

class Room(models.Model):
    _name = "optesis.room"
    _description = "optesis room"

    name = fields.Char(String="Local", required=True, size=50)
    description = fields.Char(String="description")
    level_id = fields.Many2one(comodel_name="optesis.level", string="Niveau", required=True)
    room_building = fields.Many2one(comodel_name="optesis.building", string="Bâtiment", required=True)
    # room_site = fields.Many2one(comodel_name="optesis.site", string="Site", required=True)


class Condition(models.Model):
    _name = "optesis.condition"
    _description = "asset's conditions"
    _sql_constraints = [('name_unique', 'unique(name)', "Cet état existe déja")]

    name = fields.Char(size=50, required=True, string="Condition")
    description = fields.Char(string="Description")


class PayingOff(models.Model):
    _name = "optesis.poff"
    _description = "paying-off table"

    description = fields.Text(string="description")
    year = fields.Integer(string="year")
    price = fields.Integer(string="price")

class History(models.Model):
    _name = 'optesis.account.asset.log'
    _description = "asset log"

    date = fields.Datetime(string="Date")
    description = fields.Char(size=500, string="Changement")
    asset_id = fields.Many2one(comodel_name="account.asset.asset", string="Immo")


class Control(models.Model):
    _name = "optesis.control"
    _description = "inventory control"

    name = fields.Char(size=100, string="Nom du controle")
    description = fields.Char(string="Description")
    asset_ids = fields.One2many("optesis.asset.asset.transient", "control_id", "Inventaires")
    # site_id = fields.Many2one(comodel_name="optesis.site", string="Site", required=True)
    building_id = fields.Many2one(comodel_name="optesis.building", string="Batiment", required=True)
    level_id = fields.Many2one(comodel_name="optesis.level", string="Niveau",required=True)
    room_id = fields.Many2one(comodel_name="optesis.room", string="Local",required=True)
    code_barre = fields.Char(string="Controle")
    created = fields.Datetime(string="Date de creation")
    service_id = fields.Many2one('optesis.service', string="Service")
    condition_id = fields.Many2one('optesis.condition', string="Etat")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'En cours'),
        ('end', 'Terminer'),
    ], string='Status', index=True, readonly=True, default='draft')

    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
    }

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('optesis.control') or '/'
        result = super(Control, self).create(vals)
        return result


    @api.multi
    def validate_control(self):
        if self.asset_ids:
            for asset in self.asset_ids:
                real_assets = self.env['account.asset.asset'].search([('code_bar','=',asset.code_bar)])
                if real_assets:
                    for real_asset in real_assets:
                        description = 'Changement '
                        if self.building_id.id != real_asset.building.id:
                            description += 'du building {} au building {}, '.format(real_asset.building.name, self.building_id.name)
                        if self.level_id.id != real_asset.level.id:
                            description += 'du niveau {} au niveau {}, '.format(real_asset.level.name, self.level_id.name)
                        if self.room_id.id != real_asset.room.id:
                            description += 'du local {} au local {}, '.format(real_asset.room.name, self.room_id.name)
                        if self.service_id.id != real_asset.service.id:
                            description += 'du service {} au service {}, '.format(real_asset.service.name, self.service_id.name)
                        if self.condition_id.id != real_asset.condition.id:
                            description += 'du condition {} au condition {}, '.format(real_asset.condition.name, self.condition_id.name)
                        log = self.env['optesis.account.asset.log']
                        log.create({'date': datetime.datetime.now(),
                                    'asset_id': real_asset.id,
                                    'description':description})
                        # update the real asset asset
                        real_asset.update({'level': self.level_id.id,
                                      'building': self.building_id.id,
                                      'room': self.room_id.id,
                                      'service':self.service_id.id,
                                      'condition': self.condition_id.id})
                        # update the transient asset asset
                        asset.update({'level': self.level_id.id,
                                      'building': self.building_id.id,
                                      'room': self.room_id.id,
                                      'service':self.service_id.id,
                                      'condition': self.condition_id.id})
            self.state = 'end'

    @api.multi
    def start_control(self):
        self.state = 'open'

    @api.multi
    @api.onchange('code_barre')
    def change_code_barre(self):
        if self.code_barre:
            assets = self.env['account.asset.asset'].search([('code_bar','=',self.code_barre)])
            if assets:
                for asset in assets:
                    if self.asset_ids:
                        find = 0
                        for line in self.asset_ids:
                            if line.code_bar == asset.code_bar:
                                find = 1
                                break
                        if find == 1:
                            self.code_barre = None
                            raise UserError(_("Enregistrement deja ajoute."))
                        else:
                            self.asset_ids += self.env['optesis.asset.asset.transient'].create(
                                        {
                                            'category_id' : asset.category_id.id,
                                            'product_id' : asset.product_id.id,
                                            'agents' : asset.agents.id,
                                            'code_bar' : asset.code_bar,
                                            'service' : asset.service.id,
                                            'condition' : asset.condition.id,
                                            'brand' : asset.brand,
                                            'specifications' : asset.specifications,
                                            'direction' : asset.direction.id,
                                            'building' : asset.building.id,
                                            'level' : asset.level.id,
                                            'room' : asset.room.id,
                                            'inventory_date' : asset.inventory_date,
                                            'asset_number' :  asset.asset_number,
                                            'old_transfert_id' : asset.old_transfert_id.id,
                                            'transfert_id' : asset.transfert_id.id,
                                            'control_id' : self._origin.id if hasattr(self, '_origin') else None,
                                            'log_ids' : asset.log_ids,
                                            'last' : asset.last,
                                            'value' : asset.value,
                                            #'date_service' : asset.date_service,
                                        })
                    else:
                        self.asset_ids += self.env['optesis.asset.asset.transient'].create(
                            {
                                'category_id' : asset.category_id.id,
                                'product_id' : asset.product_id.id,
                                'agents' : asset.agents.id,
                                'code_bar' : asset.code_bar,
                                'service' : asset.service.id,
                                'condition' : asset.condition.id,
                                'brand' : asset.brand,
                                'specifications' : asset.specifications,
                                'direction' : asset.direction.id,
                                'building' : asset.building.id,
                                'level' : asset.level.id,
                                'room' : asset.room.id,
                                'inventory_date' : asset.inventory_date,
                                'asset_number' :  asset.asset_number,
                                'old_transfert_id' : asset.old_transfert_id.id,
                                'transfert_id' : asset.transfert_id.id,
                                'control_id' : self._origin.id if hasattr(self, '_origin') else None,
                                'log_ids' : asset.log_ids,
                                'last' : asset.last,
                                'value' : asset.value,
                                #'date_service' : asset.date_service,
                            })
                self.code_barre = None
            else:
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.asset.asset',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'context': {
                        'default_code_bar': self.code_barre,
                        'default_service': self.service_id.id,
                        'default_building': self.building_id.id,
                        'default_level': self.level_id.id,
                        'default_room': self.room_id.id,
                        'default_condition': self.condition_id.id,
                    },
                    'target': 'new',
                }


class Asset(models.Model):
    _name = "account.asset.asset"
    _inherit = "account.asset.asset"
    _description = "optesis asset first module"
    _order = "code_bar"
    _sql_constraints = [('code_bar_unique', 'unique(code_bar)', "can't be duplicate the value of code bar")]


    name = fields.Char(string='Nom', required=False)

    category_id = fields.Many2one(comodel_name="account.asset.category", string="Famille", required=False)

    product_id = fields.Many2one(comodel_name="product.template", string="Standard")

    description = fields.Text()

    agents = fields.Many2one(comodel_name='optesis.agent', string='Nom')

    value = fields.Float(string="Prix")

    reference = fields.Char(string="Référence")

    date_assignation = fields.Date(string="date d'assignation")

    commissioning = fields.Date(string="date de commision")

    type = fields.Selection([('fixed', 'Fix'),
                             ('capital','Tangible capital')])

    code_bar = fields.Char(string="Code barre", default=None, default_focus=True)

    service = fields.Many2one(comodel_name="optesis.service", string="Service")

    condition = fields.Many2one(comodel_name="optesis.condition", string="Condition")

    brand = fields.Char(string="Marque")

    specifications = fields.Char(string="spécifications")

    # department = fields.Many2one(comodel_name="optesis.department", string="Département")

    direction = fields.Many2one(comodel_name="optesis.direction", string="Direction")

    # site = fields.Many2one(comodel_name="optesis.site", string="Site")

    building = fields.Many2one(comodel_name="optesis.building", string="Bâtiment")

    level = fields.Many2one(comodel_name="optesis.level", string="Niveau")

    room = fields.Many2one(comodel_name="optesis.room", string="Local")

    date_disposal = fields.Date(string=" Date d'acquisition")

    num_facture_vente = fields.Char(string="Numéro facture de vente")

    type_disposal = fields.Selection([('vente','Sell'), ('achat', 'Buy')], string="Type de cession")

    value_disposal = fields.Integer(string="valeur de la session")

    buyer = fields.Many2one(comodel_name='optesis.employee', string="Agent")

    est_amortie = fields.Boolean(string="Année de cession ")

    history = fields.Many2many(comodel_name="optesis.agent", string="history")

    inventory_date = fields.Date(required=True, default=datetime.date.today(), string="Date d'inventaire", readonly=True, store=True)


    asset_number = fields.Char(string="Numéro immo", )

    old_transfert_id = fields.Many2one(comodel_name="optesis.asset.transfert")

    transfert_id = fields.Many2one(comodel_name="optesis.asset.transfert")

    control_id = fields.Many2one(comodel_name="optesis.control", string="Control")

    log_ids = fields.One2many("optesis.account.asset.log", "asset_id", "historiques")

    last = fields.Datetime(default=datetime.datetime.now(), string='derniere modification')

    num_bc = fields.Char("Numéro BC")

    num_br = fields.Char("Numéro BR")

    _defaults = {
        'asset_number': lambda obj, cr, uid, context: '/',
    }

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('account.asset.asset') or '/'
        vals['asset_number'] = seq
        # vals['name'] = vals['code_bar'] or "/"
        return super(Asset, self).create(vals)


    @api.multi
    def asset_renew(self):
        next_record = self
        new_form = {
            'type': 'ir.actions.act_window',
            'res_model': 'account.asset.asset',
            'view_type': 'form',
            'view_mode': 'form',
            'context':{
                       'default_product_id': self.product_id.id,
                       'default_direction':self.direction.id,
                       'default_category_id':self.category_id.id,
                       'default_service':self.service.id,
                       'default_room': self.room.id,
                       'default_building': self.building.id,
                       'default_level': self.level.id,
                       'default_condition': self.condition.id,
                       'default_value':self.value,
                       'default_partner_id':self.partner_id.id,
                       'default_num_bc':self.num_bc,
                       'default_num_br':self.num_br,
                       },
            'target': 'new',
        }
        return new_form


    @api.onchange("product_id")
    def onchange_name(self):
        self.category_id = self.product_id.asset_category_id
        self.last = datetime.datetime.now()

    @api.onchange("service")
    def onchange_service(self):
        dir = self.env["optesis.direction"].browse(self.service.direction_id.id)
        self.direction = dir.id
        self.last = datetime.datetime.now()

    # @api.onchange("department")
    # def onchange_department(self):
    #     dir = self.env["optesis.direction"].browse(self.department.direction_id.id)
    #     self.direction = dir.id
    #     self.last = datetime.datetime.now()

    @api.onchange("product_id","agents","code_bar","condition","brand","specifications","direction","building","level","room","inventory_date","asset_number")
    def onchange_last(self):
        self.last = datetime.datetime.now()

    @api.multi
    def pass_to_openall(self):
        if self.filtered(lambda inv: inv.state != 'draft'):
            raise UserError(_("Opération impossible les immobilisations ne sont pas en brouillon"))
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        for record in self.env['account.asset.asset'].browse(active_ids):
            record.write({'state': 'open'})

    @api.multi
    def pass_to_closeall(self):
        if self.filtered(lambda inv: inv.state != 'open'):
            raise UserError(_("Opération impossible les immobilisations ne sont pas confirmé"))
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        for record in self.env['account.asset.asset'].browse(active_ids):
            record.write({'state': 'close'})



class asset_account_invoice_line(models.Model):
    _inherit="account.invoice.line"

    # @api.v7
    @api.one
    def asset_create(self):
        return True

class StockMove(models.Model):
    _inherit = "stock.move"

    immo_id = fields.Many2one("account.asset.asset", "Immobilisation")

    @api.one
    def asset_create(self):
        _logger.info("fonction_asset_create")
        if self.product_id.asset_category_id:
            vals = {
                'name': self.product_id.name,
                'product_id': self.product_id.id,
                'code': False,
                'category_id': self.product_id.asset_category_id.id,
                'value': self.price_unit,
                'partner_id': self.picking_id.partner_id.id,
                'company_id': self.picking_id.company_id.id,
                'num_bc':self.picking_id.origin,
                'num_br':self.picking_id.name,
                # 'currency_id': False,
                'date': self.picking_id.date,
                # 'invoice_id': self.picking_id.id,
            }
            changed_vals = self.env['account.asset.asset'].onchange_category_id_values(vals['category_id'])
            vals.update(changed_vals['value'])
            asset = self.env['account.asset.asset'].create(vals)
            if self.product_id.asset_category_id.open_asset:
                asset.validate()
        return True


class Picking(models.Model):
    _inherit = "stock.picking"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('confirmer', 'Confirmé'),
        ('done', 'Done'),
        ('immo', 'Immobilisé'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, track_visibility='onchange',
        help=" * Draft: not confirmed yet and will not be scheduled until confirmed.\n"
             " * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows).\n"
             " * Waiting: if it is not ready to be sent because the required products could not be reserved.\n"
             " * Ready: products are reserved and ready to be sent. If the shipping policy is 'As soon as possible' this happens as soon as anything is reserved.\n"
             " * Done: has been processed, can't be modified or cancelled anymore.\n"
             " * Cancelled: has been cancelled, can't be confirmed anymore.")

    immo = fields.Boolean("Contient Immo", compute="detect_immo")
    is_immo = fields.Selection([('immo', 'Oui'), ('no_immo','Non')], 'Est immobilisé', default='no_immo')

    def create_immo(self):
        _logger.info("fonction_create_immo")
        for line in self.move_ids_without_package:
            line.asset_create()
        self.state = "immo"
        self.is_immo = "immo"

    @api.depends("move_ids_without_package")
    def detect_immo(self):
        if self.move_ids_without_package:
            for line in self.move_ids_without_package:
                if line.product_id.asset_category_id:
                    self.immo = True
                    break



    # def _action_done(self):
    #     self.filtered(lambda move: move.state == 'draft')._action_confirm()  # MRP allows scrapping draft moves
    #     moves = self.exists().filtered(lambda x: x.state not in ('done', 'cancel'))
    #     moves_todo = self.env['stock.move']
    #
    #     # Cancel moves where necessary ; we should do it before creating the extra moves because
    #     # this operation could trigger a merge of moves.
    #     for move in moves:
    #         if move.quantity_done <= 0:
    #             if float_compare(move.product_uom_qty, 0.0, precision_rounding=move.product_uom.rounding) == 0:
    #                 move._action_cancel()
    #
    #     # Create extra moves where necessary
    #     for move in moves:
    #         if move.state == 'cancel' or move.quantity_done <= 0:
    #             continue
    #         # extra move will not be merged in mrp
    #         if not move.picking_id:
    #             moves_todo |= move
    #         moves_todo |= move._create_extra_move()
    #
    #     # Split moves where necessary and move quants
    #     for move in moves_todo:
    #         # To know whether we need to create a backorder or not, round to the general product's
    #         # decimal precision and not the product's UOM.
    #         rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
    #         if float_compare(move.quantity_done, move.product_uom_qty, precision_digits=rounding) < 0:
    #             # Need to do some kind of conversion here
    #             qty_split = move.product_uom._compute_quantity(move.product_uom_qty - move.quantity_done, move.product_id.uom_id, rounding_method='HALF-UP')
    #             new_move = move._split(qty_split)
    #             for move_line in move.move_line_ids:
    #                 if move_line.product_qty and move_line.qty_done:
    #                     # FIXME: there will be an issue if the move was partially available
    #                     # By decreasing `product_qty`, we free the reservation.
    #                     # FIXME: if qty_done > product_qty, this could raise if nothing is in stock
    #                     try:
    #                         move_line.write({'product_uom_qty': move_line.qty_done})
    #                     except UserError:
    #                         pass
    #             move._unreserve_initial_demand(new_move)
    #     moves_todo.mapped('move_line_ids')._action_done()
    #     # Check the consistency of the result packages; there should be an unique location across
    #     # the contained quants.
    #     for result_package in moves_todo\
    #             .mapped('move_line_ids.result_package_id')\
    #             .filtered(lambda p: p.quant_ids and len(p.quant_ids) > 1):
    #         if len(result_package.quant_ids.mapped('location_id')) > 1:
    #             raise UserError(_('You cannot move the same package content more than once in the same transfer or split the same package into two location.'))
    #     picking = moves_todo and moves_todo[0].picking_id or False
    #     moves_todo.write({'state': 'done', 'date': fields.Datetime.now()})
    #     moves_todo.mapped('move_dest_ids')._action_assign()
    #
    #     # We don't want to create back order for scrap moves
    #     if all(move_todo.scrapped for move_todo in moves_todo):
    #         return moves_todo
    #
    #     if picking:
    #         picking._create_backorder()
    #
    #     moves_todo.asset_create()
    #     return moves_todo

class ParticularReport(models.AbstractModel):
    _name = 'report.optesis.asset_print_inventory'

    @api.multi
    def render_html(self, data=None):
        asset_number_per_room = []
        rooms_ids = []
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('optimo_account_asset_stock.asset_print_inventory')
        for asset in self.pool[report.model].browse(self._cr, self._uid, self._ids, context=self._context):
            if asset.room.id not in rooms_ids:
                assets = self.env[report.model].search([('id','in', self._ids),('room','=', asset.room.id)])
                asset_number_per_room.append(len(assets))
                rooms_ids.append(asset.room.id)

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'rooms': self.env['optesis.room'].browse(rooms_ids),
            'asset_number_per_room' : asset_number_per_room,
        }

        return report_obj.render('optimo_account_asset_stock.asset_print_inventory', docargs)


class OptesisAssetTransiant(models.Model):
    _name = "optesis.asset.asset.transient"
    _description = "optesis asset first module transient"

    # name = fields.Char(string='Nom', required=False)

    category_id = fields.Many2one(comodel_name="account.asset.category", string="Famille", required=False)

    product_id = fields.Many2one(comodel_name="product.template", string="Standard")

    agents = fields.Many2one(comodel_name='optesis.agent', string='Employé')

    code_bar = fields.Char(string="Code barre", default=None)

    service = fields.Many2one(comodel_name="optesis.service", string="Service")

    condition = fields.Many2one(comodel_name="optesis.condition", string="État")

    brand = fields.Char(string="Marque")

    specifications = fields.Char(string="Spécifications")

    direction = fields.Many2one(comodel_name="optesis.direction", string="Direction")

    building = fields.Many2one(comodel_name="optesis.building", string="Bâtiment")

    level = fields.Many2one(comodel_name="optesis.level", string="Niveau")

    room = fields.Many2one(comodel_name="optesis.room", string="Local")

    inventory_date = fields.Date(required=True, default=datetime.date.today(), string="Date d'inventaire", readonly=True, store=True)

    asset_number = fields.Char(string="Numéro immo", readonly=True)

    old_transfert_id = fields.Many2one(comodel_name="optesis.asset.transfert")

    transfert_id = fields.Many2one(comodel_name="optesis.asset.transfert")

    control_id = fields.Many2one(comodel_name="optesis.control", string="Control")

    log_ids = fields.One2many("optesis.account.asset.log", "asset_id", "historiques")

    last = fields.Datetime(default=datetime.datetime.now(), string='derniere modification', )

    value = fields.Float("Valeur Brute")

    #date_service = fields.Date("Date de Mise en service")
