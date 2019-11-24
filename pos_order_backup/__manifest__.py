# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Order Backup/Restore",
  "summary"              :  "With the help of this module, the POS user can restore the last POS order from the local in case the data is lost due in case of connection failure.",
  "category"             :  "Point of Sale",
  "version"              :  "1.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Order-Backup-Restore.html",
  "description"          :  """Odoo POS Order Backup/Restore
POS restore order
Restore order in POS
Backup order data in POS
POS fail safe
POS connection backup
POS connection fail backup""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_order_backup",
  "depends"              :  [
                             'point_of_sale',
                             'wk_wizard_messages',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/template.xml',
                             'views/point_of_sale_view.xml',
                             'wizard/import_orders_wizard_view.xml',
                            ],
  "qweb"                 :  ['static/src/xml/pos.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}