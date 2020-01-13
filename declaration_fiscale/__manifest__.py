{
    'name': 'Declarations Fiscales',
    'author': 'Optesis SA',
    'version': '1.4.0',
    'category': 'account',
    'description': """
    permet de faire une descripotion ...
""",
    'summary': 'Module de ...',
    'sequence': 1,
    'depends': ['base','account','account_accountant','l10n_pcgo'],
    'data': [
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/company_view.xml',
        'wizards/individual_view.xml',
        'wizards/loyer_view.xml',
        'views/menu_view.xml',
        'views/period_view.xml',
        'views/report.xml',
        'views/custom_format.xml',
        'views/report_trimestre_tier.xml',
        'views/report_annuel_tier.xml',
        'views/report_trimestre_loyer.xml',
        'views/report_annuel_loyer.xml',
     ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}