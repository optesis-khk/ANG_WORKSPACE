from odoo import api, models, fields


class materials(models.AbstractModel):
    _name = 'report.optesis.asset_print_inventory'

    @api.multi
    def render_html(self, data=None):
        asset_number_per_room = []
        rooms_ids = []
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('optimo_account_asset.asset_print_inventory')
        for asset in self.pool[report.model].browse(self._cr, self._uid, self._ids, context=self._context):
            if asset.room_id.id not in rooms_ids:
                assets = self.env[report.model].search([('id','in', self._ids),('room_id','=', asset.room_id.id)])
                asset_number_per_room.append(len(assets))
                rooms_ids.append(asset.room_id.id)

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'rooms': self.env['optesis.room'].browse(rooms_ids),
            'asset_number_per_room' : asset_number_per_room,
        }

        return report_obj.render('optimo_account_asset.asset_print_inventory', docargs)
