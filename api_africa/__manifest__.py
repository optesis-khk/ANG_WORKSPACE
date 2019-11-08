# -*- coding: utf-8 -*-
{
    'name': 'Api Africa',
    'version': '12.0.1',
    'summary': """Api Africa Report""",
    'description': """ """,
    'category': 'Advanced Reporting',
    'author': 'Optesis SA',
    'maintainer': 'Optesis',
    'company': 'Optesis SA',
    'website': 'https://www.optesis.com',
    'depends': ['base','sale_management'],
    'data': [
        'views/api_africa_external_view.xml',
        'views/api_africa_internal_report.xml',
        'views/custom_format.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}