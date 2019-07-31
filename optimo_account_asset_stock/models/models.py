  #-*- coding:utf-8 -*-
from odoo import models, fields, api, osv
from odoo.exceptions import ValidationError
import datetime
import time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_round, float_is_zero


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

    @api.one
    def asset_create(self):
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
                'date': self.picking_id.min_date,
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

    def create_immo(self):
        for line in self.move_lines:
            line.asset_create()
        self.state = "immo"

    @api.depends("move_lines")
    def detect_immo(self):
        if self.move_lines:
            for line in self.move_lines:
                if line.product_id.asset_category_id:
                    self.immo = True
                    break

    # @api.multi
    # def action_done(self):
    #     """ Process completely the moves given and if all moves are done, it will finish the picking. """
    #     self.filtered(lambda move: move.state == 'draft').action_confirm()
    #
    #     Uom = self.env['product.uom']
    #     Quant = self.env['stock.quant']
    #
    #     pickings = self.env['stock.picking']
    #     procurements = self.env['procurement.order']
    #     operations = self.env['stock.pack.operation']
    #
    #     remaining_move_qty = {}
    #
    #     for move in self:
    #         if move.picking_id:
    #             pickings |= move.picking_id
    #         remaining_move_qty[move.id] = move.product_qty
    #         for link in move.linked_move_operation_ids:
    #             operations |= link.operation_id
    #             pickings |= link.operation_id.picking_id
    #
    #     # Sort operations according to entire packages first, then package + lot, package only, lot only
    #     operations = operations.sorted(key=lambda x: ((x.package_id and not x.product_id) and -4 or 0) + (x.package_id and -2 or 0) + (x.pack_lot_ids and -1 or 0))
    #
    #     for operation in operations:
    #
    #         # product given: result put immediately in the result package (if False: without package)
    #         # but if pack moved entirely, quants should not be written anything for the destination package
    #         quant_dest_package_id = operation.product_id and operation.result_package_id.id or False
    #         entire_pack = not operation.product_id and True or False
    #
    #         # compute quantities for each lot + check quantities match
    #         lot_quantities = dict((pack_lot.lot_id.id, operation.product_uom_id._compute_quantity(pack_lot.qty, operation.product_id.uom_id)
    #         ) for pack_lot in operation.pack_lot_ids)
    #         if operation.pack_lot_ids and float_compare(sum(lot_quantities.values()), operation.product_qty, precision_rounding=operation.product_uom_id.rounding) != 0.0:
    #             raise UserError(_('You have a difference between the quantity on the operation and the quantities specified for the lots. '))
    #
    #         quants_taken = []
    #         false_quants = []
    #         lot_move_qty = {}
    #
    #         prout_move_qty = {}
    #         for link in operation.linked_move_operation_ids:
    #             prout_move_qty[link.move_id] = prout_move_qty.get(link.move_id, 0.0) + link.qty
    #
    #         # Process every move only once for every pack operation
    #         for move in prout_move_qty.keys():
    #             # TDE FIXME: do in batch ?
    #             move.check_tracking(operation)
    #
    #             # TDE FIXME: I bet the message error is wrong
    #             if not remaining_move_qty.get(move.id):
    #                 raise UserError(_("The roundings of your unit of measure %s on the move vs. %s on the product don't allow to do these operations or you are not transferring the picking at once. ") % (move.product_uom.name, move.product_id.uom_id.name))
    #
    #             if not operation.pack_lot_ids:
    #                 preferred_domain_list = [[('reservation_id', '=', move.id)], [('reservation_id', '=', False)], ['&', ('reservation_id', '!=', move.id), ('reservation_id', '!=', False)]]
    #                 quants = Quant.quants_get_preferred_domain(
    #                     prout_move_qty[move], move, ops=operation, domain=[('qty', '>', 0)],
    #                     preferred_domain_list=preferred_domain_list)
    #                 Quant.quants_move(quants, move, operation.location_dest_id, location_from=operation.location_id,
    #                                   lot_id=False, owner_id=operation.owner_id.id, src_package_id=operation.package_id.id,
    #                                   dest_package_id=quant_dest_package_id, entire_pack=entire_pack)
    #             else:
    #                 # Check what you can do with reserved quants already
    #                 qty_on_link = prout_move_qty[move]
    #                 rounding = operation.product_id.uom_id.rounding
    #                 for reserved_quant in move.reserved_quant_ids:
    #                     if (reserved_quant.owner_id.id != operation.owner_id.id) or (reserved_quant.location_id.id != operation.location_id.id) or \
    #                             (reserved_quant.package_id.id != operation.package_id.id):
    #                         continue
    #                     if not reserved_quant.lot_id:
    #                         false_quants += [reserved_quant]
    #                     elif float_compare(lot_quantities.get(reserved_quant.lot_id.id, 0), 0, precision_rounding=rounding) > 0:
    #                         if float_compare(lot_quantities[reserved_quant.lot_id.id], reserved_quant.qty, precision_rounding=rounding) >= 0:
    #                             lot_quantities[reserved_quant.lot_id.id] -= reserved_quant.qty
    #                             quants_taken += [(reserved_quant, reserved_quant.qty)]
    #                             qty_on_link -= reserved_quant.qty
    #                         else:
    #                             quants_taken += [(reserved_quant, lot_quantities[reserved_quant.lot_id.id])]
    #                             lot_quantities[reserved_quant.lot_id.id] = 0
    #                             qty_on_link -= lot_quantities[reserved_quant.lot_id.id]
    #                 lot_move_qty[move.id] = qty_on_link
    #
    #             remaining_move_qty[move.id] -= prout_move_qty[move]
    #
    #         # Handle lots separately
    #         if operation.pack_lot_ids:
    #             # TDE FIXME: fix call to move_quants_by_lot to ease understanding
    #             self._move_quants_by_lot(operation, lot_quantities, quants_taken, false_quants, lot_move_qty, quant_dest_package_id)
    #
    #         # Handle pack in pack
    #         if not operation.product_id and operation.package_id and operation.result_package_id.id != operation.package_id.parent_id.id:
    #             operation.package_id.sudo().write({'parent_id': operation.result_package_id.id})
    #
    #
    #     # Check for remaining qtys and unreserve/check move_dest_id in
    #     move_dest_ids = set()
    #     for move in self:
    #         if float_compare(remaining_move_qty[move.id], 0, precision_rounding=move.product_id.uom_id.rounding) > 0:  # In case no pack operations in picking
    #             move.check_tracking(False)  # TDE: do in batch ? redone ? check this
    #
    #             preferred_domain_list = [[('reservation_id', '=', move.id)], [('reservation_id', '=', False)], ['&', ('reservation_id', '!=', move.id), ('reservation_id', '!=', False)]]
    #             quants = Quant.quants_get_preferred_domain(
    #                 remaining_move_qty[move.id], move, domain=[('qty', '>', 0)],
    #                 preferred_domain_list=preferred_domain_list)
    #             Quant.quants_move(
    #                 quants, move, move.location_dest_id,
    #                 lot_id=move.restrict_lot_id.id, owner_id=move.restrict_partner_id.id)
    #
    #         # If the move has a destination, add it to the list to reserve
    #         if move.move_dest_id and move.move_dest_id.state in ('waiting', 'confirmed'):
    #             move_dest_ids.add(move.move_dest_id.id)
    #
    #         if move.procurement_id:
    #             procurements |= move.procurement_id
    #
    #         # unreserve the quants and make them available for other operations/moves
    #         move.quants_unreserve()
    #
    #     # Check the packages have been placed in the correct locations
    #     self.mapped('quant_ids').filtered(lambda quant: quant.package_id and quant.qty > 0).mapped('package_id')._check_location_constraint()
    #
    #     # set the move as done
    #     self.write({'state': 'done', 'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
    #     procurements.check()
    #     # assign destination moves
    #     if move_dest_ids:
    #         # TDE FIXME: record setise me
    #         self.browse(list(move_dest_ids)).action_assign()
    #
    #     pickings.filtered(lambda picking: picking.state == 'done' and not picking.date_done).write({'date_done': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
    #
    #     context = dict(self.env.context)
    #
    #     pickings.move_lines.with_context(context).asset_create()
    #
    #     return True

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
