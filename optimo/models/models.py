#-*- coding:utf-8 -*-
from odoo import models, fields, api, osv, _
from odoo.exceptions import ValidationError, UserError
import datetime
import logging

_logger = logging.getLogger(__name__)


class Direction(models.Model):
    _name = "optesis.direction"
    _description = "optesis direction"
    #_sql_constraints = [('name_unique', 'unique(name)', "Cette direction existe déja")]

    name = fields.Char(String="direction", required=True, size=50)
    description = fields.Char(String="description")
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)


class department(models.Model):
    _name = "optesis.department"
    _description = "optesis departement"
    #_sql_constraints = [('name_unique', 'unique(name)', "Ce département existe déja")]

    name = fields.Char(String="Département", required=True, size=50)
    description = fields.Char(String="description")
    direction_id = fields.Many2one(comodel_name="optesis.direction", string="Direction", required=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)

class Service(models.Model):
    _name = "optesis.service"
    _description = "optesis service"
    #_sql_constraints = [('name_unique', 'unique(name)', "Ce service existe déja")]

    name = fields.Char(String="Service", required=True, size=50)
    description = fields.Char(String="description")
    direction_id = fields.Many2one(comodel_name="optesis.direction", string="Direction", required=True)
    department_id = fields.Many2one(comodel_name="optesis.department", string="Département", required=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)



class Agent(models.Model):
    _name = "optesis.agent"
    _description = "user database"

    name = fields.Char(string="Nom et Prénom",required="True", size=100)
    service = fields.Many2one(comodel_name="optesis.service", string="Service", required=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)

class Region(models.Model):
    _name = 'optesis.region'

    name = fields.Char('Nom', required=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)

class Localite(models.Model):
    _name = 'optesis.localite'

    name = fields.Char('Nom', required=True)
    region_id = fields.Many2one(comodel_name="optesis.region", string="Région", required=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)

class Commune(models.Model):
    _name = 'optesis.commune'

    name = fields.Char('Nom', required=True)
    localite_id = fields.Many2one(comodel_name="optesis.localite", string="Localité", required=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)



class Site(models.Model):
    _name = "optesis.site"
    _description = "optesis site"
    #_sql_constraints = [('name_unique', 'unique(name)', "ce site existe déja")]

    name = fields.Char(String="Site", required=True, size=50)
    address = fields.Char(String="Addresse")
    region_id = fields.Many2one(comodel_name="optesis.region", string="Région", required=True)
    localite_id = fields.Many2one(comodel_name="optesis.localite", string="Localite", required=True)
    commune_id = fields.Many2one(comodel_name="optesis.commune", string="Commune", required=True)
    description = fields.Char(String="description")
    long = fields.Float(string="Longitude")
    lat = fields.Float("Latitude")
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)


class Building(models.Model):
    _name = "optesis.building"
    _description = "optesis building"

    name = fields.Char(String="Bâtiment", required=True, size=50)
    description = fields.Char(String="description")
    site_id = fields.Many2one(comodel_name="optesis.site", string="Site", required=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)

class Level(models.Model):
    _name = "optesis.level"
    _description = "optesis level"

    name = fields.Char(String="Niveau", required=True, size=50)
    description = fields.Char(String="description")
    building_id = fields.Many2one(comodel_name="optesis.building", string="Bâtiment", required=True)
    site_level = fields.Many2one(comodel_name="optesis.site", string="Site", required=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)

class Room(models.Model):
    _name = "optesis.room"
    _description = "optesis room"

    name = fields.Char(String="Local", required=True, size=50)
    description = fields.Char(String="description")
    level_id = fields.Many2one(comodel_name="optesis.level", string="Niveau", required=True)
    room_building = fields.Many2one(comodel_name="optesis.building", string="Bâtiment", required=True)
    room_site = fields.Many2one(comodel_name="optesis.site", string="Site", required=True)
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)

class Articles(models.Model):
    _name = "optesis.product"
    _description = "standard des immobilisations"
    #_sql_constraints = [('name_unique', 'unique(name)', 'Ce standard existe déja')]

    name = fields.Char(string="Standard", required=True)
    category_id = fields.Many2one("optesis.family", "Famille", required=True)
    description = fields.Char(string="Description")
    price = fields.Float(string="Prix", )
    product_id = fields.Many2one(comodel_name="product.product", string="articles")
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)

    @api.model
    def create(self, vals):
        product = self.env['product.product'].create({'name':vals['name']})
        vals['product_id'] = product.id
        return super(Articles, self).create(vals)

class Famille(models.Model):
    _name = "optesis.family"
    _description = "Famille de l'immobilisation"
    #_sql_constraints = [('name_unique', 'unique(name)', "Cette catégorie existe déja")]

    name = fields.Char(string="Famille", required=True)
    description = fields.Char(string="description")
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)


class Condition(models.Model):
    _name = "optesis.condition"
    _description = "asset's conditions"
    #_sql_constraints = [('name_unique', 'unique(name)', "Cet état existe déja")]

    name = fields.Char(size=50, required=True, string="Condition")
    description = fields.Char(string="Description")
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)

class History(models.Model):
    _name = 'optesis.account.asset.log'
    _description = "asset log"

    date = fields.Datetime(string="Date")
    description = fields.Char(size=500, string="Description")
    asset_id = fields.Many2one(comodel_name="optesis.asset.asset", string="Immo")
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)


class Control(models.Model):
    _name = "optesis.control"
    _description = "inventory control"

    name = fields.Char(size=100, string="Nom du controle")
    description = fields.Char(string="Description")
    asset_ids = fields.One2many("optesis.asset.asset.transient", "control_id", "Inventaires")
    site_id = fields.Many2one(comodel_name="optesis.site", string="Site", required=True)
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
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)


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
                real_assets = self.env['optesis.asset.asset'].search([('code_bar','=',asset.code_bar)])
                if real_assets:
                    for real_asset in real_assets:
                        description = 'Changement '
                        if self.site_id.id != real_asset.site.id:
                            description += 'du site {} au site {}, '.format(real_asset.site.name, self.site_id.name)
                        if self.building_id.id != real_asset.building.id:
                            description += 'du building {} au building {}, '.format(real_asset.building.name, self.building_id.name)
                        if self.level_id.id != real_asset.level.id:
                            description += 'du niveau {} au niveau {}, '.format(real_asset.level.name, self.level_id.name)
                        if self.room_id.id != real_asset.room.id:
                            description += 'du local {} au local {}, '.format(real_asset.room.name, self.room_id.name)
                        if self.service_id.id != real_asset.service.id:
                            description += 'du service {} au service {}, '.format(real_asset.service.name, self.service_id.name)
                        if asset.condition.id != real_asset.condition.id:
                            description += 'du condition {} au condition {}, '.format(real_asset.condition.name, asset.condition.name)
                        log = self.env['optesis.account.asset.log']
                        log.create({'date': datetime.datetime.now(),
                                    'asset_id': real_asset.id,
                                    'description':description})
                        # update the real asset asset
                        real_asset.update({'site': self.site_id.id,
                                      'level': self.level_id.id,
                                      'building': self.building_id.id,
                                      'room': self.room_id.id,
                                      'service':self.service_id.id,
                                      'condition': asset.condition.id})
                        # update the transient asset asset
                        asset.update({'site': self.site_id.id,
                                      'level': self.level_id.id,
                                      'building': self.building_id.id,
                                      'room': self.room_id.id,
                                      'service':self.service_id.id,
                                      'condition': asset.condition.id})
            self.state = 'end'

    @api.multi
    @api.onchange('code_barre')
    def change_code_barre(self):
        if self.code_barre:
            assets = self.env['optesis.asset.asset'].search([('code_bar','=',self.code_barre)])
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
                                            'family_id' : asset.family_id.id,
                                            'product_id' : asset.product_id.id,
                                            'agents' : asset.agents.id,
                                            'code_bar' : asset.code_bar,
                                            'service' : asset.service.id,
                                            'condition' : self.condition_id.id,
                                            'brand' : asset.brand,
                                            'specifications' : asset.specifications,
                                            'department' : asset.department.id,
                                            'direction' : asset.direction.id,
                                            'site' : asset.site.id,
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
                                            'date_service' : asset.date_service,
                                        })
                    else:
                        self.asset_ids += self.env['optesis.asset.asset.transient'].create(
                            {
                                'family_id' : asset.family_id.id,
                                'product_id' : asset.product_id.id,
                                'agents' : asset.agents.id,
                                'code_bar' : asset.code_bar,
                                'service' : asset.service.id,
                                'condition' : self.condition_id.id,
                                'brand' : asset.brand,
                                'specifications' : asset.specifications,
                                'department' : asset.department.id,
                                'direction' : asset.direction.id,
                                'site' : asset.site.id,
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
                                'date_service' : asset.date_service,
                            })
                self.code_barre = None
                #self.condition_id = None
            else:
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'optesis.asset.asset',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'context': {
                        'default_code_bar': self.code_barre,
                        'default_service': self.service_id.id,
                        'default_site': self.site_id.id,
                        'default_building': self.building_id.id,
                        'default_level': self.level_id.id,
                        'default_room': self.room_id.id,
                        'default_condition': self.condition_id.id,
                    },
                    'target': 'new',
                }

    @api.multi
    def start_control(self):
        self.state = 'open'





class OptesisAsset(models.Model):
    _name = "optesis.asset.asset"
    _description = "optesis asset first module"
    _sql_constraints = [('code_bar_unique', 'unique(company_id, code_bar)', "can't be duplicate the value of code bar")]

    #name = fields.Char(string='Nom', required=False)

    family_id = fields.Many2one(comodel_name='optesis.family', string="Famille")

    product_id = fields.Many2one(comodel_name="optesis.product", string="Standard")

    agents = fields.Many2one(comodel_name='optesis.agent', string='Employé')

    code_bar = fields.Char(string="Code barre", default=None)

    service = fields.Many2one(comodel_name="optesis.service", string="Service")

    condition = fields.Many2one(comodel_name="optesis.condition", string="État")

    brand = fields.Char(string="Marque")

    specifications = fields.Char(string="Spécifications")

    department = fields.Many2one(comodel_name="optesis.department", string="Département")

    direction = fields.Many2one(comodel_name="optesis.direction", string="Direction")

    site = fields.Many2one(comodel_name="optesis.site", string="Site")

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

    date_service = fields.Date("Date de Mise en service")

    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)

    _defaults = {
        'asset_number': lambda obj, cr, uid, context: '/',
    }

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('optesis.asset.asset') or '/'
        vals['asset_number'] = seq
        return super(OptesisAsset, self).create(vals)

    @api.multi
    def asset_renew(self):
        next_record = self
        new_form = {
            'type': 'ir.actions.act_window',
            'res_model': 'optesis.asset.asset',
            'view_type': 'form',
            'view_mode': 'form',
            #'context': "{'default_CHILD_FIELD' : 'module.id' }",
            #'res_id': next_record.ids[0],
            'context':{#'default_product_id': next_record._get_previous_record(name=self.product_id.name, model="optesis.product"),
                       'default_product_id': self.product_id.id,
                       'default_direction':self.direction.id,
                       'default_site': self.site.id,
                       'default_family_id':self.family_id.id,
                       'default_department': self.department.id,
                       'default_service':self.service.id,
                       'default_room': self.room.id,
                       'default_building': self.building.id,
                       'default_level': self.level.id,
                       'default_condition': self.condition.id,
                       'default_value' : self.value,
                       'default_date_service' : self.date_service,
                       },
            'target': 'new',
        }
        return new_form

    @api.multi
    def action_save(self):
        #your code
        self.ensure_one()
        #close popup
        return {'type': 'ir.actions.act_window_close'}

    @api.onchange("product_id")
    def onchange_name(self):
        self.family_id = self.product_id.category_id
        self.last = datetime.datetime.now()

    @api.onchange("service")
    def onchange_service(self):
        dep = self.env["optesis.department"].browse(self.service.department_id.id)
        self.department = dep.id
        self.last = datetime.datetime.now()

    @api.onchange("department")
    def onchange_department(self):
        dir = self.env["optesis.direction"].browse(self.department.direction_id.id)
        self.direction = dir.id
        self.last = datetime.datetime.now()

    @api.onchange("family_id","agents","code_bar","condition","brand","specifications","direction","site","building","level","room","inventory_date","asset_number")
    def onchange_last(self):
        self.last = datetime.datetime.now()


class ParticularReport(models.AbstractModel):
    _name = 'report.optesis.asset_print_inventory'

    @api.multi
    def render_html(self, data=None):
        asset_number_per_room = []
        rooms_ids = []
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('optimo.asset_print_inventory')
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

        return report_obj.render('optimo.asset_print_inventory', docargs)



class OptesisAssetTransiant(models.Model):
    _name = "optesis.asset.asset.transient"
    _description = "optesis asset first module transient"

    # name = fields.Char(string='Nom', required=False)

    family_id = fields.Many2one(comodel_name='optesis.family', string="Famille")

    product_id = fields.Many2one(comodel_name="optesis.product", string="Standard")

    agents = fields.Many2one(comodel_name='optesis.agent', string='Employé')

    code_bar = fields.Char(string="Code barre", default=None)

    service = fields.Many2one(comodel_name="optesis.service", string="Service")

    condition = fields.Many2one(comodel_name="optesis.condition", string="État")

    brand = fields.Char(string="Marque")

    specifications = fields.Char(string="Spécifications")

    department = fields.Many2one(comodel_name="optesis.department", string="Département")

    direction = fields.Many2one(comodel_name="optesis.direction", string="Direction")

    site = fields.Many2one(comodel_name="optesis.site", string="Site")

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

    date_service = fields.Date("Date de Mise en service")

    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)
