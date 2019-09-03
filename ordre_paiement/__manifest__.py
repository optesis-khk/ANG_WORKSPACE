{
    'name': 'Ordre de Paiement',
    'author': 'Optesis',
    'version': '3.3.0',
    'category': 'Tools',
    'description': """
    permet de faire une descripotion ...
""",
    'summary': 'Module de ...',
    'sequence': 9,
    'depends': ['base', 'account_accountant', 'l10n_pcgo', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/ordre_paiement_view.xml',
        'views/account_invoice_view.xml',
        'views/stock_picking_view.xml',
        'views/sequence.xml',
     ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
