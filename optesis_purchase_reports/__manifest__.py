# -*- encoding: utf-8 -*-

{
  "name": "Quotation & purchase reports",
  "version": "10.0",
  "author": "Optesis SA",
  "category": 'Quotation & purchase reports',
  "description": """Quotation & purchase reports""",
  'website': 'http://www.optesis.com',
  'init_xml': [],
  "depends": ['base', 'sale', 'purchase', 'account', 'web'],
  'data': [

    'report/paper_format.xml',
    'report/menu_purchase_order.xml',
    #'views/report_sale_order_modern_feelings.xml',
    'views/report_purchase_order.xml',
    'views/template.xml',

  ],
  'qweb': [

  ],
  'web_preload': True,
  'demo_xml': [],
  'installable': True,
  'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
