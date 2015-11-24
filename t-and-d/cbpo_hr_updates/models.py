# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import fields, osv
from datetime import datetime
import time
from dateutil import parser

class cbpo_hr_updates(osv.osv):
    _inherit = 'hr.employee'

    # def onchange_birth_date(self, cr, uid, ids, DOB, context=None):
    #     current_date = datetime.now()
    #     current_year = current_date.year
    #     birth_date = parser.parse(DOB)
    #
    #     if birth_date.year > current_year - 120 and birth_date.year < current_year - 18:
    #         current_age = current_year - birth_date.year
    #     else:
    #         raise osv.except_osv(('Invalid DOB'), ('Please enter a valid DATE OF BIRTH'))
    #     val = {
    #         'cbpo_age':current_age
    #     }
    #     return {'value': val}
    def _age_compute(self, cr, uid, ids, field_name,field_value,arg, context=None):
        records = self.browse(cr, uid, ids, context=context)
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            age=0
            if r.birthday:
                age = (datetime.now()-datetime.strptime(r.birthday,"%Y-%m-%d")).days/356
            result[r.id] = age

        return result

    _columns = {
        # Public Information Tab
        'cbpo_unversity_id': fields.many2one('cbpo.universiyt', 'University'),
        'cbpo_faculty_id': fields.many2one('cbpo.faculty', 'Faculty'),
        'cbpo_graduation_year': fields.char('Graduation Year'),
        'cbpo_grade': fields.char('Grade'),
        'cbpo_department_id': fields.char('College Department'),
        'cbpo_pres': fields.text('Pros'),
        'cbpo_cons': fields.text('Cons'),

        # Personal Information Tab
        'cbpo_phone': fields.char('Phone'),
        'cbpo_work_mobile': fields.char('Work Mobile'),
        'cbpo_personal_mobile': fields.char('Personal Mobile'),
        'cbpo_relation': fields.char('Relation'),
        'cbpo_emergency_num': fields.char('Emergency Number'),
        'cbpo_age': fields.function(_age_compute, type='char', method=True, string='Age', store=True),
        'cbpo_miliary': fields.selection([('served', 'Served'), ('postponed', 'Postponed'), ('exemption', 'Exemption')], 'Military status'),

        # HR settings Tab
        'cbpo_social_ins_num': fields.integer('Social Insurance Number'),
        'cbpo_social_basic_ins': fields.float('Social Basic Insurance'),
        'cbpo_social_var_ins': fields.float('Social Variable Insurance'),
		'cbpo_date': fields.date('Date'),

    }



cbpo_hr_updates()


class cbpo_universiyt(osv.osv):
    _name = 'cbpo.universiyt'

    _columns = {
        'name': fields.char('University name'),
    }


cbpo_universiyt()


class cbpo_faculty(osv.osv):
    _name = 'cbpo.faculty'

    _columns = {
        'name': fields.char('Faculty name'),
    }


cbpo_faculty()

# class cbpo_holidays_updates(osv.osv):
#     _inherit = 'hr.holidays'
#
# cbpo_holidays_updates()
