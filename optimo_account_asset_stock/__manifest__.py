{
    'name': 'Optimo Account Asset Stock',
    'author': 'OPTESIS SA',
    'version': '1.3.1',
    'category': 'Asset',
    'description': """
Ce module permet de faire l'inventaire des immobilisations de votre entreprise d'une manière structurée, fiable et intuitive
""",
    'summary': 'Module d\'inventaire ',
    'sequence': 9,
    'depends': ['base','account_asset','product', 'account', 'purchase', 'stock','compta_matiere'],
    'data': [
      'security/security.xml',
      'security/ir.model.access.csv',
      'views/optesis_views.xml',
      'views/stock_picking.xml',
      'views/employee.xml',
      'views/site.xml',
      'views/direction.xml',
      'views/document.xml',
      'views/optesis.xml',
      'views/transfert.xml',
      'views/sequence_control.xml',
      'views/sequence_immo.xml',
      'views/sequence_transfert.xml',

    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
