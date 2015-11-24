# -*- coding: utf-8 -*-
{
    'name': "Cbpo Attendance & Payslip Compute",

    'summary': """
        Attendance , Calculate the deduct & Overtime  monthly salaries ,
        Fingetprint Data ,payslip        """,

    'description': """
        - This module calculates the monthly salaries to employees

        - After pull data from fingetprint
        - And the integration of fingerprint data to record attendance and leave in odoo
        - And doing a monthly record of discounts and Overtime
        - and it can be linked to payslip
        - Manage Maximum Deduction
    """,

    'author': "Core Bpo : Hashem ALy  smart.hashem@gmail.com",
    'website': "http://www.core-bpo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '1.3',


    # any module necessary for this one to work correctly
    'depends': ['base', 'hr','hr_attendance','hr_contract','report'  ,'hr_holidays','cbpo_hr_holidays'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml','hr_attendance2_view.xml','hr_attendance_update.xml','hr_fingerprint_configration_view.xml','cbpo_fid_view.xml',
        'hr_discipline_view.xml','reports.xml','holidays_templates.xml', 'calendar.xml',
        'report/report_payslipdetails2.xml','report/report_attend.xml',




    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}