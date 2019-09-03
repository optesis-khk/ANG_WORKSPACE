# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Supply Request",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Odoo Community Association (OCA)",
    "version": "1.1.0",
    "summary": "Use this module to have notification of requirements of "
               "materials and/or external services and keep track of such "
               "requirements.",
    "category": "Supply Management",
    "depends": [
        "purchase",
        "product",
        "procurement",
        "stock_analytic"
    ],
    "data": [
        "security/supply_request.xml",
        "security/ir.model.access.csv",
        "data/supply_request_sequence.xml",
        "data/supply_request_data.xml",
        "views/supply_request_view.xml",
        "reports/report_supplyrequests.xml",
        "views/supply_request_report.xml",
    ],
    'demo': [
        "demo/supply_request_demo.xml",
    ],
    "license": 'LGPL-3',
    'installable': True
}
