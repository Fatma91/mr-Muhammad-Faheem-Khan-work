# -*- coding: utf-8 -*-
{
    'name': "Project Coustom",

    'description': """
        Project Customazion.
    """,

    'author': "Core BPO",
    'website': "http://www.core-bpo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','project_issue','cbpo_sales'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'project_project_view.xml',
        'project_tasks_view.xml',
        'project_issue_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}