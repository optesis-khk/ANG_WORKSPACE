{
    'name': 'Declarations Fiscales',
    'author': 'Optesis SA',
    'version': '12.0.0.0',
    'category': 'account',
    'description': """
    permet de faire une descripotion ...
""",
    'summary': 'Module de ...',
    'sequence': 1,
    'depends': ['base','account','account_accountant'],
    'data': [
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/company_view.xml',
        'wizards/individual_view.xml',
        'wizards/loyer_view.xml',
        'views/menu_view.xml',
        'views/report.xml',
        'views/report_trimestre_tier.xml',
     ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
