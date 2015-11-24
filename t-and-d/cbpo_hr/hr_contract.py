# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import datetime
from dateutil.relativedelta import relativedelta
import time



class cbpo_hr_contract4(osv.osv):

    _inherit="hr.contract"

    #
    def _compute_plus_month(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)
        for obj in self.browse(cr, uid, ids, context=context):
            date_end=obj.date_end

            if(date_end):
                mydate =  datetime.datetime.strptime(date_end, "%Y-%m-%d")
                next_month = mydate+  relativedelta(months=-1)
                next_month_day=next_month.date()
                end_res=str(next_month_day)
                res[obj.id]=  end_res

            else:
                return res
        return res

    def _compute_week(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)
        for obj in self.browse(cr, uid, ids, context=context):
            date_end=obj.trial_date_end

            if(date_end):
                mydate =  datetime.datetime.strptime(date_end, "%Y-%m-%d")
                next_month = mydate+  relativedelta(days=-14)
                next_month_day=next_month.date()
                end_res=str(next_month_day)
                res[obj.id]=  end_res

            else:
                return res
        return res



    _columns = {

        # 'date_end_plus_month': fields.date('date_end_plus_month'),
        #
        'date_end_week': fields.function(_compute_week, type='date', string='date_end_week', store=True),
        'date_end_month': fields.function(_compute_plus_month, type='date', string='date_end_month', store=True),
        'net_salary': fields.float('Net Salary'),
        'medical_insurance_number': fields.char('Medical Insurance Number'),
        'medical_insurance_amount': fields.float('Medical Insurance Amount'),



    }


cbpo_hr_contract4()


