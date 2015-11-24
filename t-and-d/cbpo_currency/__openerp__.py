# -*- coding: utf-8 -*-
{
    'name': "Calculate Currency",

    'description': """
        Calculating Currency in jurnal entry and landing cost
    """,

    'author': "Core BPO",
    'website': "http://www.core-bpo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','stock','stock_landed_costs'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'calc_currency.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}