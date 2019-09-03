{
    'name': 'Comptabilité Matière',
    'author': 'Optesis',
    'version': '2.2.0',
    'category': 'Tools',
    'description': """
    permet de faire une descripotion ...
""",
    'summary': 'Module de ...',
    'sequence': 4,
    'depends': ['base','stock'],
    'data': [
        'data/data.xml',
        'report/report.xml',
        'report/pv_reception.xml',
        'report/bon_entree.xml',
        'report/fiche_detenteur.xml',
        'report/bordereau_affectation.xml',
        'report/bordereau_mutation.xml',
        'report/bordereau_mouvement.xml',
        'report/bon_sortie.xml',
        'report/pv_vente.xml',
        'report/pv_reforme.xml',
        'views/stock_picking_view.xml',
        'views/menu_view.xml'
     ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
