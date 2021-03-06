# -*- coding: utf-8 -*-
{
    'name': "cbpo_sales",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Core BPO",
    'website': "http://www.core-bpo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','product','account','analytic','cbpo_product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml','sale_order.xml',
        'custom_sale_order_report.xml',
        'sale_quotation_seq.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}