# -*- coding: utf-8 -*-
{
    'name': "Core-BPO_warehouse",

    'summary': """
        Provide a new fields on stock moves, allowing to manage the orders of moves
in a picking""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Core BPO",
    'website': "http://www.core-bpo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'warehouse',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale', 'sale_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'stock_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}