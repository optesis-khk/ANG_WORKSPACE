# -*- coding: utf-8 -*-
{
    "name": "Stocks Access Rules",
    "version": "12.0.1.0.1",
    "category": "Warehouse",
    "author": "Odoo Tools",
    "website": "https://odootools.com/apps/12.0/stocks-access-rules-232",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "stock"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/stock_view.xml",
        "views/res_users_view.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to restrict users' access to stocks, locations and warehouse operations",
    "description": """
    The app goal is to manage users access to locations and product stocks. The tool let you better control movements and
organize geographically distributed warehouse system

    The tool is often used along with the <a href="https://apps.odoo.com/apps/modules/12.0/product_stock_balance">module 'Stock by Locations'</a>
    A user would see only the locations and the stocks placed <i>either</i> on his/her locations and their children, <i>or on the locations without accepted users stated</i>
    Define users on the form of locations or locations on a the form of users. Both approaches would lead to the same results. <i>Be cautious: if no user is defined on a location form, those locations and the related stocks would be visible for everybody</i>
    If a user has a right for this location, he/she has an access to all its child locations
    The rights are controlled for locations, stock quants (available inventories), pickings, stock moves, picking types (operations)
    The rules are for everybody except Administrator and users with special rights 'Super Warehouse Manager'. Those users would see all the locations disregarding settings
    The app is fully compatible with other Odoo Core Apps, including <i>Point of Sale (POS)</i>
    The app support multi companies' environment
    Define users who may access that locations and its child locations
    If a user has an access to this location, he/she has rights for its child locations
    Restriction rules are applied for all users except Super Warehouse Managers
    Define both users for locations and locations for users
    Inventory levels without restrictions
    Users are able to sale, purchase or transfer stocks only from their locations
    Warehouse operations without restrictions
    Available operations for this user (based on default in and out locations)
    Stock pickings without restrictions
    Pickings of this user
    Full list of internal locations
    Limited access to locations
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "28.0",
    "currency": "EUR",
}