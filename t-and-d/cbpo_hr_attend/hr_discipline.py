# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import psycopg2

class hr_discipline(osv.osv):

    _name="hr.discipline"

    def _from_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)
        m=0
        h=0
        for obj in self.browse(cr, uid, ids, context=context):

            arr_str=obj.fromtime.split(":")
            if(len(arr_str)>1 and len(arr_str[1])==2 and len(arr_str[0])==2 ):

                m=int(arr_str[1])
                h=int(arr_str[0])*60
                #
                res[obj.id] = int(h+m)
            # except psycopg2.DatabaseError, e:
            else:
                raise osv.except_osv('Error!', 'Error In Data Time \n You Can Write Like 09:30 \n 9 hours and 30 mins')

                print 'error'
        return res
    def _to_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)
        m=0
        h=0
        for obj in self.browse(cr, uid, ids, context=context):
            arr_str=obj.totime.split(":")
            if(len(arr_str)>1 and len(arr_str[1])==2 and len(arr_str[0])==2 ):

                m=int(arr_str[1])
                h=int(arr_str[0])*60

                res[obj.id] = int(h+m)
            else:
                raise osv.except_osv('Error!', 'Error In Data Time \n You Can Write Like 09:30 \n 9 hours and 30 mins')

                print 'error'
        return res
    def _get_new_id(self, cr, uid, ids):
        data_ids=self.pool.get('hr.discipline').search(cr,uid,[('name' , '>' , 0)] ,order='name')
        res=len(data_ids)+1
      
            
        return res   
    _columns = {
        'name' : fields.integer('ID'),
        'daytype': fields.selection([('late_in', 'Late In'), ('late_out', 'Late Out'),('early_in', 'Early In'), ('early_out', 'Early Out')], 'Day Type', required=True),

        'deductype': fields.selection([('Hours', 'Hours'),  ('Ratio', 'Ratio')], 'Deduct Type', required=True),
        'fromtime': fields.char('From time' ,size=5, required=True),
        'totime': fields.char('From time' ,size=5, required=True),
        
        
        't_from': fields.function(_from_compute, type='integer', string='From', store=True, select=1, size=32),
        't_to': fields.function(_to_compute, type='integer', string='To', store=True, select=1, size=32),

        'd1': fields.float('Deduct 1'),
        'l1': fields.float('Leaves 1' ),
        'd2': fields.float('Deduct 2' ),
        'l2': fields.float('Leaves 2' ),
        'd3': fields.float('Deduct 3' ),
        'l3': fields.float('Leaves 3' ),
        'd4': fields.float('Deduct 4' ),
        'l4': fields.float('Leaves 4' ),
        'calendar_id' : fields.many2one("resource.calendar", "Calendar ID" , required=True ),

    }
    _defaults = {
    'fromtime': '00:00',
    'totime': '00:00',
    'name': _get_new_id
    }

    _order = 'daytype desc ,calendar_id desc , t_from asc'
#     _sql_constraints = [('Id_unique', 'unique(name)', 'ID  already exists')]

hr_discipline()