{
    'name': 'Facture Paps',

    'description': """
               Gacture Paps
            """,

    'author': 'OPTESIS SA BY ANG',
    'website': "http://www.Optesis.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '1.2.0',
    'category': 'Test',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    'data': [
        'views/paps_devis_internal_report.xml',
        'views/paps_report_internal_report.xml',
        'views/paps_report_external_view.xml',
        'views/custom_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

}
