# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import psycopg2
import calendar
from datetime import date


from datetime import date
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
        'totime': fields.char('To time' ,size=5, required=True),
        
        
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


class hr_allowance(osv.osv):

    _name="hr.allowance"

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
                raise osv.except_osv('Error!', 'Error In Data Time TO \n You Can Write Like 09:30 \n 9 hours and 30 mins')

                print 'error'
        return res




    _columns = {
        'name' : fields.char('Name',required=True),
        'daytype': fields.selection([('late_in', 'Late In'), ('late_out', 'Late Out'),('early_in', 'Early In'), ('early_out', 'Early Out')], 'Day Type', required=True),

        'totime': fields.char('To time' ,size=5, required=True),

        'fromtime': fields.char('From time' ,size=5, required=True),

        'tt_to': fields.function(_to_compute, type='integer', string='To', store=True, select=1, size=32),
        'tt_from': fields.function(_from_compute, type='integer', string='From', store=True, select=1, size=32),

        'repetition': fields.integer('Repetition' ,size=5, required=True),

        'calendar_id' : fields.many2one("resource.calendar", "Calendar ID" , required=True ),

    }
    _defaults = {
    'repetition': '1',
    'totime': '00:00',
    'fromtime': '00:00',

    }

    _order = 'calendar_id desc , tt_from asc'
#     _sql_constraints = [('Id_unique', 'unique(name)', 'ID  already exists')]

hr_allowance()




class hr_excuse(osv.osv):

    _name="hr.excuse"
    _inherit = ['ir.needaction_mixin']

    def _needaction_domain_get(self   , cr, uid , context=None):
        """
        Show a count of sick horses on the menu badge.
        An exception: don't show the count to Bob,
        because he worries too much!
        """
        # if self.env.user.name == "Bob":
        #     return False  # don't show to Bob!
        return [('state', '=', 'Draft')]


    def _compute_allow(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)
        m=0
        h=0
        for obj in self.browse(cr, uid, ids, context=context):
            type=obj.type
            day_start=0
            day_end=0
            this_day_int=0
            if(type=='Excuse'   ):
                arr_str=obj.timeexcuse.split(":")
                arr_day=obj.day.split("-")
                year=int(arr_day[0])
                month=int(arr_day[1])
                day=int(arr_day[2])

                this_day_int=int(arr_day[0])*10000+int(arr_day[1])*100+int(arr_day[2])
                employee_id=obj.employee_id.id



                # last_day=calendar.monthrange(year, month)[1]
                # end_date = date(year,month,last_day)

                if(len(arr_str)>1 and len(arr_str[1])==2 and len(arr_str[0])==2 ):

                    mint=int(arr_str[1])
                    hour_mint=int(arr_str[0])*60
                    total_mints=mint+hour_mint
                    # res[obj.id] = int(h+m)


                    company_ids=self.pool.get('res.users').read(cr, uid, uid, ["company_id"])
                    cmmppny=company_ids['company_id'][0]
                    company_data=self.pool.get('res.company').read(cr, uid, cmmppny, ["max_excuse_count","max_excuse_minutes","start_day","tt_in","tt_out"])
                    mystartday=int(company_data['start_day'])
                    tt_in=int(company_data['tt_in'])
                    tt_out=int(company_data['tt_out'])
                    max_excuse_count=company_data['max_excuse_count']
                    max_excuse_minutes=company_data['max_excuse_minutes']


                    y=year
                    m=month
                    m1=0
                    y1=0
                    if(mystartday>1):
                        mystartdayend=mystartday+1
                        myendday0=str(mystartdayend)
                        mystartday0=str(company_data['start_day'])
                        startday_int=int(mystartday0)
                        # y=int(wizared.year)
                        # m=int(wizared.month)

                        if(m>1):
                            if(day>startday_int):
                                a=''
                                m1=m+1
                                day_s1=y*10000+m1*100+int(myendday0)
                                day_s2=y*10000+m*100+int(mystartday0)
                                day_end =int(y)*10000+int(m)*100+int(mystartday0)
                                day_start=int(y)*10000+int(m1)*100+int(myendday0)
                            else:
                                b=''
                                m1=m-1
                                day_s1=y*10000+m1*100+int(myendday0)
                                day_s2=y*10000+m*100+int(mystartday0)
                                day_start=int(y)*10000+int(m)*100+int(mystartday0)-1
                                day_end=int(y)*10000+int(m1)*100+int(myendday0)-1

                        else:
                            m1=1
                            y1=y-1


                    else:
                        m1=m
                        day_s1=y*10000+m1*100+int(1)
                        day_s2=y*10000+m*100+int(last_day)
                        day_start=int(y)*10000+int(m)*100+int(1)
                        day_end=int(y)*10000+int(m1)*100+int(last_day)


                    a=''
                    # company_ids=self.pool.get('hr.excuse').read(cr, uid, uid, ["company_id"])
                    total_data_time=0

                    #  ('time_excuse','>', day_end) ,('employee_id' , '=' , employee_id),('type','=','Excuse'),('state','=','Approved')
                    # 'state': fields.selection([('Draft', 'Draft'), ('Approved',
                    excuse_ids=self.pool.get('hr.excuse').search(cr,uid,[('type','=','Excuse'),('state','=','Approved'),('day_excuse','>=', day_end) ,('day_excuse','<=', day_start) ,('employee_id' , '=' , employee_id)],order='day asc')
                    excuse_count=len(excuse_ids)
                    if(excuse_count>0):
                        for excuseID in excuse_ids:

                            row_data_excuse = self.pool.get('hr.excuse').read(cr, uid, excuseID,['time_excuse'])
                            time_excuse=row_data_excuse['time_excuse']
                            if(time_excuse>0):
                                total_data_time=total_data_time+time_excuse




                    else:
                        b=''

                    # now we can cheek count and total mints ..
                    if(excuse_count>max_excuse_count):
                        raise  osv.except_osv('Error!', 'The Total Excuse is = { '+str(excuse_count)+' } \n ' +
                             'The Max Excuse is = { '+str(max_excuse_count)+' } \n'+
                                ' You Can Not Have Many Excuse. \n'+' From Date : '+str(day_end)+'  To Date : '+str(day_start)+' . ')

                    if(total_data_time>max_excuse_minutes):
                        raise  osv.except_osv('Error!', 'The Total Mints Excuse is = { '+str(total_data_time)+' } \n The Max Mints Excuse is = { '+str(max_excuse_minutes)+' } \n'
                                           +' Do Not Have a Sufficient Balance Of Time Excuse . \n'+' From Date : '+str(day_end)+'  To Date : '+str(day_start)+' . ')

                    max_excuse_count=company_data['max_excuse_count']
                    max_excuse_minutes=company_data['max_excuse_minutes']
                    c=''

                else:
                    raise osv.except_osv('Error!', 'Error In Date Time Excuse TO \n You Can Write Like 01:30 \n 1 hours and 30 mins')

                    print 'error'
        return res

    def _toexcuse_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)
        m=0
        h=0
        for obj in self.browse(cr, uid, ids, context=context):
            arr_str=obj.timeexcuse.split(":")
            if(len(arr_str)>1 and len(arr_str[1])==2 and len(arr_str[0])==2 ):

                m=int(arr_str[1])
                h=int(arr_str[0])*60

                res[obj.id] = int(h+m)
            else:
                raise osv.except_osv('Error!', 'Error In Date Time Excuse TO \n You Can Write Like 01:30 \n 1 hours and 30 mins')

                print 'error'
        return res

    def _dayexcuse_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)
        day_s=0

        for obj in self.browse(cr, uid, ids, context=context):
            arr_str=obj.day.split("-")
            if(len(arr_str)>0 ):



                day_s=int(arr_str[0])*10000+int(arr_str[1])*100+int(arr_str[2])



                res[obj.id] = int(day_s)
            else:
                raise osv.except_osv('Error!', 'Error In Date   ')

                print 'error'
        return res

    def action_approved(self, cr, uid, ids, context=None):
        obj=self.browse(cr, uid, ids[0], context=context)
        this_daytype=obj.daytype
        this_day=obj.day
        this_employee_id=obj.employee_id.id

        if(this_daytype=='full_day'):
            a=''
            attend2_ids=self.pool.get('hr.attendance2').search(cr,uid,[('employee_id' , '=' , this_employee_id),('name' , '=' , this_day) ,('action','=','Mission'),('state','=','Mission'),('diff_time_in','=','Mission'),('diff_time_out','=','Mission') ],order='employee_id asc' )
            self.pool.get('hr.attendance2').unlink(cr, uid, attend2_ids)

            self.pool.get('hr.attendance2').create(cr,uid,{'employee_id':this_employee_id, 'name':this_day, 'action':'Mission' ,  'state':'Mission' ,'diff_time_in':'Mission','diff_time_out':'Mission'})

            return self.write(cr, uid, ids[0], {'state': 'Approved'}, context=context)
        else:
            b=''
            return self.write(cr, uid, ids[0], {'state': 'Approved'}, context=context)


    def action_draft(self, cr, uid, ids, context=None):

        obj=self.browse(cr, uid, ids[0], context=context)
        this_daytype=obj.daytype
        this_day=obj.day
        this_employee_id=obj.employee_id.id

        if(this_daytype=='full_day'):
            a=''
            attend2_ids=self.pool.get('hr.attendance2').search(cr,uid,[('employee_id' , '=' , this_employee_id),('name' , '=' , this_day) ,('action','=','Mission'),('state','=','Mission'),('diff_time_in','=','Mission'),('diff_time_out','=','Mission') ],order='employee_id asc' )
            self.pool.get('hr.attendance2').unlink(cr, uid, attend2_ids)
            # self.pool.get('hr.attendance2').create(cr,uid,{'employee_id':this_employee_id, 'name':this_day, 'action':'Mission' ,  'state':'Mission' ,'diff_time_in':'Mission','diff_time_out':'Mission'})

            return self.write(cr, uid, ids, {'state': 'Draft'}, context=context)
        else:
            return self.write(cr, uid, ids, {'state': 'Draft'}, context=context)

    def _employee_get(self, cr, uid, context=None):
        emp_id = context.get('default_employee_id', False)
        if emp_id:
            return emp_id
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return False
    _columns = {
        'name' : fields.char('Excuse Name',required=True),
        'type': fields.selection([('Excuse', 'Excuse'),('Mission', 'Mission')], 'Excuse / Mission',required=True),
        'daytype': fields.selection([('late_in', 'Late In'),  ('early_out', 'Early Out'),('full_day','Full Day')], 'Day Type', required=True),

        'timeexcuse': fields.char('Time' ,size=5, required=True),


        'time_excuse': fields.function(_toexcuse_compute, type='integer', string='Time Excuse', store=True, select=1, size=32),

        'day': fields.date('Day Excuse' , required=True),
        'state': fields.selection([('Draft', 'Draft'), ('Approved', 'Approved')], 'State' ),


        'day_excuse': fields.function(_dayexcuse_compute, type='integer', string='Day Excuse', store=True, select=1, size=32),

        'employee_id': fields.many2one('hr.employee', "Employee", required=True, select=True),
        'note':fields.text('Note'),
         # 'allow': fields.integer('allow'),
        'allow': fields.function(_compute_allow, type='integer', string='allow', store=True, select=1, size=32),


    }
    _defaults = {

    'timeexcuse': '00:00',
    'type': 'Excuse',
    'daytype': 'late_in',
    'state':'Draft',
    'employee_id': _employee_get,


    }
    _order = 'day asc ,type asc , daytype asc , state asc, employee_id asc'




hr_excuse()

