# -*- coding: utf-8 -*-
{
    'name': "CBPO core sales updates",

    'summary': """
        CBPO core sales updates""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Core BPO",
    'website': "http://www.core-bpo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}