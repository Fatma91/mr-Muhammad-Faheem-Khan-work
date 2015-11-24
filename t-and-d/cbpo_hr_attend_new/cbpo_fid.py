# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields, osv
from datetime import datetime,timedelta , date
import time
 

class cbpo_contract(osv.osv):
    _inherit = 'resource.calendar'
    _description = "Core-BPO  discipline Lines in resource.calendar "
    _columns = {
        'discipline_ids': fields.one2many('hr.discipline', 'calendar_id', 'Disciplines', copy=True),
    }



class project_task_works2(osv.osv):
    _inherit = 'project.task.work'
    def _myday_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)


        for obj in self.browse(cr, uid, ids, context=context):

            if(str(obj.date)!='' ):
                date=obj.date
                res[obj.id] = time.strftime('%Y-%m-%d', time.strptime(date, '%Y-%m-%d %H:%M:%S'))




            else:
                res[obj.id] =''


        return res

    def _user_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)


        for obj in self.browse(cr, uid, ids, context=context):
            task_id=obj.task_id.id
            # project_tasks=self.pool.get('project.task').browse(cr,uid,[task_id] , context=context)
            project_task_data=self.pool.get('project.task').read(cr, uid, task_id, ["user_id"])
            user_id=project_task_data['user_id'][0]
            res[obj.id]=user_id


        return res

    def _project_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)


        for obj in self.browse(cr, uid, ids, context=context):
            task_id=obj.task_id.id
            project_tasks=self.pool.get('project.task').browse(cr,uid,[task_id] , context=context)
            project_id=project_tasks.project_id.id
            projects=self.pool.get('project.project').browse(cr,uid,[project_id] , context=context)
            res[obj.id]=projects.name

        return res



    _columns = {
        'user': fields.function(_user_compute, type='char', string='user', store=True, select=1, size=32),
        'day': fields.function(_myday_compute, type='char', string='Day', store=True, select=1, size=64),
        'project_name': fields.function(_project_compute, type='char', string='projectname', store=True, select=1, size=64),
    }



#

class cbpo_fid(osv.osv):
    _inherit = 'hr.employee'
    _description = "Core-BPO FingerPrint ID "

    # function check for fingerPrintId not exists in table hr.employee ;    
    def _check_unique_fpid(self, cr, uid, ids, context=None):
        wizareds = self.browse(cr, uid, ids,context=None)
        wizared = wizareds[0]
        fid=wizared.cbpo_fingerPrintId
        if(fid==0):
            return True

        userids=self.pool.get('hr.employee').search(cr,uid,[('cbpo_fingerPrintId' , '=' , fid)],order=None)
        if((len(userids)) > 1 ):
            return False
        else:
            return True
      
    _columns = {
        # this field for id from   Finger Print ;           
        'cbpo_fingerPrintId':fields.integer('fingerPrintId'),
        'currency_id': fields.many2one('res.currency', 'Currency', help="Currency."),

    }
    _defaults = {
        'currency_id':'77',
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

