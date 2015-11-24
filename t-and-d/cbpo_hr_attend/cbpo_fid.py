# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields, osv


 

class cbpo_contract(osv.osv):
    _inherit = 'resource.calendar'
    _description = "Core-BPO  discipline Lines in resource.calendar "
    _columns = {
        'discipline_ids': fields.one2many('hr.discipline', 'calendar_id', 'Disciplines', copy=True),
    }
class cbpo_fid(osv.osv):
    _inherit = 'hr.employee'
    _description = "Core-BPO FingerPrint ID "

    # function check for fingerPrintId not exists in table hr.employee ;    
    def _check_unique_fpid(self, cr, uid, ids, context=None):
        wizareds = self.browse(cr, uid, ids,context=None)
        wizared = wizareds[0]
        fid=wizared.cbpo_fingerPrintId
        userids=self.pool.get('hr.employee').search(cr,uid,[('cbpo_fingerPrintId' , '=' , fid)],order=None)
        if((len(userids)) > 1):
            return False
        else:
            return True
      
    _columns = {
        # this field for id from   Finger Print ;           
        'cbpo_fingerPrintId':fields.integer('fingerPrintId'),
    }
    
    _sql_constraints = [('cbpo_fingerPrintId_unique', 'unique(cbpo_fingerPrintId)', 'Finger Print Id  already exists')]
    _constraints = [(_check_unique_fpid, 'Finger Print Id already exists', ['cbpo_fingerPrintId'])]

cbpo_fid()


class hr_finger_conf(osv.osv_memory):
    _name = 'hr.finger.conf'
    _columns = {
            'db': fields.selection([('Microsoft Access Driver (*.mdb, *.accdb)', 'MS Access Win64'), ('Microsoft Access Driver (*.mdb)', 'MS Access Win32'),('oracle', 'Oracle'),('mysql','MySQL'),('postgres','Postgres')], "DataBase Type"),    
            'path':fields.char('Access Path',size=200),
            'dbname':fields.char('DataBase Name',size=200),
            'username':fields.char('User Name',size=15),
            'password':fields.char('password',size=200,password="True"),
            'active': fields.boolean('Active'),
            'otherdata':fields.char('Other Data',size=200),
             
            

    }
    _defaults = {
    'path': 'c://attend/att2000.mdb',
    'dbname': 'Checkinout'
    }
   
hr_finger_conf()

