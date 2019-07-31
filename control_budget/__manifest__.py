{
    'name': 'Control Budget',
    'author': 'OPTESIS SA',
    'version': '1.3.0',
    'category': 'Tools',
    'description': """
Ce module permet de faire le control budgetaire
""",
    'summary': 'Comptabilite',
    'sequence': 9,
    'depends': ['base','account','account_reports','analytic','account_analytic_default','account_budget','purchase','purchase_request','purchase_request_to_rfq','procurement_jit'],
    'data': [
        'data/approve_mail_template.xml',
        'data/refuse_mail_template.xml',
        'security/purchase_security.xml',
        'wizard/purchase_order_refuse_wizard_view.xml',
        'views/account_budget_view.xml',
        'views/account_analytic_account_view.xml',
        'views/purchase_view.xml',
        'views/res_company_view.xml',
    ],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
