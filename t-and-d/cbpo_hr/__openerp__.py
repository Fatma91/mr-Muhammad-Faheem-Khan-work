# -*- coding: utf-8 -*-
{
    'name': "Core Hr Update",

    'summary': """
      Core Hr Update""",

    'description': """
      Core Hr Update
    """,

    'author': "Core Bpo :: BY HASHEM.Aly",
    'website': "http://www.core-bpo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'hr',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_contract','hr'],

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