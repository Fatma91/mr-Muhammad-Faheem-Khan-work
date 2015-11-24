# -*- coding: utf-8 -*-
from openerp.osv import fields, osv





class cbpo_hr_employee4(osv.osv):

    _inherit="hr.employee"

    #
    def _compute_id(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)
        count_id=0
        for obj in self.browse(cr, uid, ids, context=context):
            if(obj.identification_id):
                count_id=len(obj.identification_id)
            if(count_id==0):
                res[obj.id] = ''
            elif(count_id!=14):
                raise osv.except_osv('Error!  Identification ID!','Identification ID : Must Be 14 characters. \nNot  '+str(count_id)+' characters.')
                print " Error!  Identification ID! "

            else:
                res[obj.id] = 'OK'
        return res



    _columns = {
        # 'id_ok': fields.char('ID_OK'),
        'id_ok': fields.function(_compute_id, type='char', string='id_ok', store=True,),
        'employment_date': fields.date('Employment Date'),
    }


cbpo_hr_employee4()
