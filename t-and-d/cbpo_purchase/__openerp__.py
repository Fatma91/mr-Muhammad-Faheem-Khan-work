# -*- coding: utf-8 -*-
{
    'name': "cbpo_purchase",

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
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'purchase_order_revision.xml',
        'purchase_sequence_view.xml',
        'purchase_quotation_seq.xml',
        'wizard_purchase_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}