# -*- coding: utf-8 -*-
{
    'name': "Test sale kanban",

    'summary': """""",

    'description': """

    """,

    'author': "abdalla",
    'website': "abdalla.mhafeez@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board', 'mail', 'sale'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'sequence_view.xml',
        # 'views/openacademy_courses.xml',
        # 'views/partner.xml',
        #
        # 'views/customer_invoice.xml',
        # 'views/openacademy_sessions.xml',
        # 'views/job_position.xml',
        # 'views/action_type_view.xml',
        # 'views/action_view.xml',
        # 'views/contract_view.xml',
        'sale_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
}
