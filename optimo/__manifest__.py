{
    'name': 'Optimo',
    'author': 'OPTESIS SA',
    'version': '3.3.1',
    'category': 'Tools',
    'description': """
Ce module permet de faire l'inventaire des immobilisations de votre entreprise d'une manière structurée, fiable et intuitive
""",
    'summary': 'Module d\'inventaire ',
    'sequence': 9,
    'depends': ['base','product'],
    'data': [
       'security/security.xml',
       'security/ir.model.access.csv',
       'views/optesis_views.xml',
       'views/employee.xml',
       'views/site.xml',
       'views/direction.xml',
       'views/document.xml',
       'views/optesis.xml',
       'views/transfert.xml',
       'security/multi_company_view.xml',
       'views/sequence_control.xml',
       'views/sequence_transfert.xml',
       'report/fiche_detenteur_header_view.xml',
       'report/fiche_detenteur_external_layout_header.xml',
       'report/custom_paper_format.xml',
       'report/fiche_detenteur.xml',
       'report/report.xml',
       'views/sequence_immo.xml',

    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
