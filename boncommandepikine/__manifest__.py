{
    'name': 'Bon de commande Pikine',

    'description': """
                ce module permet de faire le Bon de commande de pikine:
                    
            """,

    'author': 'OPTESIS SA BY ANG',
    'website': "http://www.Optesis.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '1.2.0',
    'category': 'Test',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'purchase'],

    'data': [
        'views/boncommande_header_footer.xml',
        'views/boncommande_external_layout.xml',
        'views/boncommande_internal_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
