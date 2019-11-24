{
    'name': 'Template Bichri',

    'description': """
               Bichri Template
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
        'views/template_Bichri_internal_report.xml',
        'views/bichri_external_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

}
