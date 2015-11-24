# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

 
import time
from array import *
#import psycopg2            # module to connect to postgresql
import os
import calendar
from datetime import date
#import pyodbc
import math
#import csv,pyodbc            # to read csv files and mdb
from subprocess import call    # to run system commands
from datetime import datetime,timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp import fields,osv, models
from openerp.osv import fields, osv
from dateutil.relativedelta import relativedelta
import unicodedata



class Update(models.Model):
    _name = 'hr.attendance.update'
    _columns = {
            'db': fields.selection([('MDBTools','MDBTools'),('Microsoft Access Driver (*.mdb)', 'MS Access Win32'),('Microsoft Access Driver (*.mdb, *.accdb)', 'MS Access Win64'), ('oracle', 'Oracle'),('mysql','MySQL'),('postgres','Postgres')], "DataBase Type"),
            'path':fields.char('Access Path',size=200),
            'dbname':fields.char('DataBase Name',size=200),
            'username':fields.char('User Name',size=15),
            'password':fields.char('password',size=200,password="True"),
            'useingconf': fields.boolean('Useing Data Wizard'),

            'day':fields.integer('Day' ,required=True),
            'day_from':fields.date('Day From' ,required=True),
            'day_to':fields.date('Day To' ,required=True),


            'month':fields.integer('Month' ,required=True),
            'year':fields.integer('Year',required=True),
            'delay':fields.integer('delay'),
            'employee_id': fields.many2one('hr.employee', "Employee", select=True),

    }


    _defaults = {


    'month':lambda *a: time.strftime('%m'),
    'day':lambda *a: time.strftime('%d'),
    'year':lambda *a: time.strftime('%Y'),
    'day_from':lambda *a: time.strftime('%Y-%m-%d'),
    'day_to':lambda *a: time.strftime('%Y-%m-%d'),
    'path': 'c://attend/att2000.mdb',
    'dbname': 'Checkinout',
    'useingconf':'False',
    'delay':'0',
    }

    def get_my_emplyee_name(self,emp):
        name=''
        employee_obj = self.pool.get('hr.employee').browse(self.cr, self.uid, [emp])
        if(employee_obj):
            name=employee_obj.name
        return name

    def print_report_attend2_done2(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}

        # company_ids=self.pool.get('res.users').read(cr, uid, uid, ["company_id"])
        # cmmppny=company_ids['company_id'][0]
        #
        #
        # company_data=self.pool.get('res.company').read(cr, uid, cmmppny, ["deduct_absence_per_day","deduct_one_in_or_out_per_day","additional_overtime_maximum","additional_overtime","additional_overtime_value","start_day","tt_in","tt_out"])
        # mystartday=int(company_data['start_day'])
        # tt_in=int(company_data['tt_in'])
        # tt_out=int(company_data['tt_out'])
        #
        #
        # overtime2=company_data['additional_overtime']
        # overtime2_value=company_data['additional_overtime_value']
        # overtime2_max=company_data['additional_overtime_maximum']
        #
        # deduct_absence_per_day=company_data['deduct_absence_per_day']
        # deduct_one_in_or_out_per_day=company_data['deduct_one_in_or_out_per_day']
        #
        #
        mydata=[]
        data=[]
        data_count=[]


        wizareds = self.browse(cr, uid, ids,context=None)
        wizared = wizareds[0]
        employee_id=wizared.employee_id.id
        # name_employee=employee_id.name
        day_hours=''
        employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
        if(len(employee_ids)>0):



            row_data_contract = self.pool.get('hr.contract').browse(cr, uid, employee_ids[0], context=context)
            lenthdata1=len(row_data_contract)
            if(lenthdata1>0):
                working_hours= row_data_contract.working_hours.id
                day_hours= row_data_contract.working_hour
        employee_data=self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
        name_employee=employee_data.name
        day_from=wizared.day_from
        day_to=wizared.day_to


        mydata.insert(1,str(name_employee))
        mydata.insert(2,wizared.day_from)
        mydata.insert(3,wizared.day_to)

        day_s1=0
        day_s2=0
        if(day_from):
            arr_day_from=day_from.split('-')

            day_s1=int(arr_day_from[0])*10000+int(arr_day_from[1])*100+int(arr_day_from[2])

        if(day_to):
            arr_day_to=day_to.split('-')

            day_s2=int(arr_day_to[0])*10000+int(arr_day_to[1])*100+int(arr_day_to[2])
        # 'name': fields.datetime('Date'),
        # 'action': fields.selection([('sign_in', 'Sign In'), ('sign_out', 'Sign Out'), ('sign_in_out', 'IN & OUT'),('Mission', 'Mission'),('Absence','Absence') , ('action','Action')], 'Action', required=True),
        # 'action_desc': fields.many2one("hr.action.reason", "Action Reason", domain="[('action_type', '=', action)]", help='Specifies the reason for Signing In/Signing Out in case of extra hours.'),
        # 'employee_id': fields.many2one('hr.employee', "Employee", required=True, select=True),
        # 'day': fields.function(_day_compute, type='char', string='Day', store=True, select=1, size=32),
        # 'dayint': fields.function(_day_int_compute, type='integer', string='Day', store=True, select=1, size=32),
        # 'schedule_time_in': fields.float('Schedule IN',help='Schedule IN .'),
        # 'schedule_time_out': fields.float('Schedule OUT',help='Schedule OUT .'),
        # 'time_in':  fields.datetime('Time IN',  help='Time IN.'),
        # 'time_out': fields.datetime('Time OUT',  help='Time OUT.'),
        # 'state': fields.selection([('in', 'In'), ('out', 'Out'), ('in_out','In & Out'),('Mission', 'Mission'),('Absence','Absence')   ], 'State', required=True),
        # 'calendar_id': fields.integer('calendar',   help='calendar.'),
        # 'absence': fields.float('Absence',help='Absence .'),
        # 'one_log': fields.float('One Log',help='One Log .'),
        # 'penalty': fields.float('Penalty',help='Penalty .'),

        # overtime_out_value

        # 'diff_time_in': fields.char('Diff IN',    help='Time Difference IN.'),
        # 'diff_time_out': fields.char('Diff Out',    help='Time Difference Out.'),
        # 'discip_in': fields.char('Discipline In',    help='Discipline In.'),
        # 'discip_in_id': fields.integer('Discipline In ID',   help='Discipline In ID.'),
        # 'discip_in_id_count': fields.integer('Discipline In Count',   help='Discipline In Count.'),
        # 'discip_out': fields.char('Discipline Out',    help='Discipline Out.'),
        # 'discip_out_id': fields.integer('Discipline Out ID',   help='Discipline Out ID.'),
        # 'discip_out_id_count': fields.integer('Discipline Out Count',   help='Discipline Out Count.'),
        # 'overtime_in': fields.char('Overtime In',    help='Overtime In.'),
        # 'overtime_in_id': fields.integer('Overtime In ID',   help='Overtime In ID.'),
        # 'overtime_in_id_count': fields.integer('Overtime In Count',   help='Overtime In Count.'),
        # 'overtime_out': fields.char('Overtime Out',    help='Overtime Out.'),
        # 'overtime_out_id': fields.integer('Overtime Out ID',   help='Overtime Out ID.'),
        # 'overtime_out_id_count': fields.integer('Overtime Out Count',   help='Overtime Out Count.'),
        #  'allowance_data': fields.char('Allowance'),
        # 'overnight': fields.integer('Overnight',   help='Overnight'),
        # 'meal': fields.integer('Meal',   help='Meal'),
        # 'excus_data': fields.char('Excus In'),
        # 'excus_data2': fields.char('Excus Out'),
        # 'mission_data': fields.char('Mission In'),
        # 'mission_data2': fields.char('Mission Out'),
        # 'compute':fields.char('compute' , size=32),

        absence_count=0

        overnight_count=0
        excus_count=0
        holiday_count=0
        meal_count=0
        penalty_count=0
        overtime_count=0.0
        deduct_in_count=0.0
        deduct_out_count=0.0
        work_time_mints_count=0
        deduct_value_count=0.0


        attend2_ids=self.pool.get('hr.attendance2').search(cr,uid,[('employee_id', '=', employee_id),('dayint' , '>=' , day_s1),('dayint' , '<=' , day_s2)  ],order='day asc' )
        for attend_id in attend2_ids:
            # row_data_one_attend2 = self.pool.get('hr.attendance2').read(cr, uid, [attend_id],[ 'state'])
            attendance2=self.pool.get('hr.attendance2').browse(cr, uid, attend_id, context=context)
            state=attendance2.state
            day=str(attendance2.day)
            name=attendance2.name
            time_in=attendance2.time_in
            time_out=attendance2.time_out
            penalty=attendance2.penalty
            one_log = float( attendance2.one_log)
            absence_absence= float(attendance2.absence)


            meal=attendance2.meal
            overnight=attendance2.overnight
            overtime_out_value=attendance2.overtime_out_value

            excus_data=attendance2.excus_data
            excus_data2=attendance2.excus_data2

            discip_in=attendance2.discip_in
            discip_out=attendance2.discip_out
            overtime_in=attendance2.overtime_in
            overtime_out=attendance2.overtime_out
            day_time=datetime.strptime(str(day),'%Y-%m-%d')
            time_in_str=''
            h_in=0
            m_in=0
            if(time_in):
                arr_time_in=time_in.split(' ')
                tiem_in_only=arr_time_in[1].split(':')
                time_in_str=str(int(tiem_in_only[0])+2)+':'+tiem_in_only[1]
                h_in=int(tiem_in_only[0])
                m_in=int(tiem_in_only[1])
            time_out_str=''
            h_out=0
            m_out=0
            if(time_out):
                arr_time_out=time_out.split(' ')
                tiem_out_only=arr_time_out[1].split(':')
                time_out_str=str(int(tiem_out_only[0])+2)+':'+tiem_out_only[1]
                h_out=int(tiem_out_only[0])
                m_out=int(tiem_out_only[1])
            work_time=''
            in_mints=h_in*60+m_in
            out_mints=h_out*60+m_out
            if(time_in and  time_out and out_mints>= in_mints):

                diff_mints=out_mints-in_mints
                diff_h=int(diff_mints/60)
                diff_m= diff_mints -( diff_h*60)
                dlm=''
                if(diff_m<10):
                    dlm='0'
                work_time=str(diff_h)+':'+dlm+str(diff_m)
                work_time_mints_count=work_time_mints_count+diff_mints


            numberofdate_int=int(day_time.strftime('%w'))
            name_day=''
            if(numberofdate_int==2):
                name_day='الثلاثاء'
            elif(numberofdate_int==3):
                name_day='الاربعاء'
            elif(numberofdate_int==4):
                name_day='الخميس'
            elif(numberofdate_int==5):
                name_day='الجمعة'
            elif(numberofdate_int==6):
                name_day='السبت'
            elif(numberofdate_int==0):
                name_day='الاحد'
            elif(numberofdate_int==1):
                name_day='الاثنين'


            project_name=''

            employee_ids=self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
            user_id=str(employee_ids.user_id.id)

            project_task_works=self.pool.get('project.task.work').search(cr,uid,[('user', '=', user_id),('day', '=', day)]  )
            for task_id in project_task_works:

                project_tasks=self.pool.get('project.task.work').browse(cr,uid,[task_id] , context=context)
                project_name=project_tasks.project_name
                # projects=self.pool.get('project.project').browse(cr,uid,[project_id] , context=context)
                # project_name=projects.name

            description=''
            deduct_in=''
            deduct_out=''
            overtime='0'
            if(overtime_out_value>0):
                overtime=str( float(overtime_out)/ float(overtime_out_value) )
                overtime_value=float( float(overtime_out)/ float(overtime_out_value) )
                overtime_count=overtime_count+overtime_value

            excus='0'
            if(excus_data and  excus_data!='' and excus_data!='0' ):
                excus='1'


            if (excus_data2 and   excus_data2!='' and  excus_data2!='0' ):
                excus='1'


            deduct_in_value=0
            deduct_out_value=0
            if(discip_in and discip_in.find('Day')==-1):
                # discip_in=float(discip_in)
                deduct_in=str( float(discip_in) / float(day_hours))
                deduct_in_value=float( float(discip_in) / float(day_hours))
                deduct_in_count=deduct_in_count+deduct_in_value



            # else:
            #
            #     dayaaaa=discip_in.split('Day');
            #     disc_days_in=float(dayaaaa[0])
            #     # compute day from leaves here
            #     disc0_in=0
            if(discip_out and discip_out.find('Day')==-1):
                # discip_out=float(discip_out)
                deduct_out=str( float(discip_out) / float(day_hours))
                deduct_out_value=float( float(discip_out) / float(day_hours))
                deduct_out_count=deduct_out_count+deduct_out_value



            project=''
            # if(name):
            #
            #     project_ids=self.pool.get('project.project').search(cr,uid,[('employee_id', '=', employee_id),
            absence='0'



            if(overnight!=0):

                overnight_count=overnight_count+1


            if(excus=='1'):
                excus_count=excus_count+1
            if(meal=='1'):
                meal_count=meal_count+1
            if(penalty=='1'):
                penalty_count=penalty_count+1

            holiday='0'
            arr_date_abs=day.split('-');
            dayint=int(arr_date_abs[0])*10000+ int(arr_date_abs[1])*100+ int(arr_date_abs[2])

            day_from=day_time.strftime('%Y-%m-%d 01:01:01')
            day_to=day_time.strftime('%Y-%m-%d 23:59:59')
            hr_holidays_ids=self.pool.get('hr.holidays').search(cr,uid,[('employee_id', '=', employee_id), ('d_f','<=',dayint ),('d_t','>=', dayint),('state','=','validate'),]  )
            hhh=len(hr_holidays_ids)
            if(hhh>0):
                holiday='1'
                holiday_count=holiday_count+1
                deduct_value=deduct_in_value+deduct_out_value
                one_log='0'

            else:
                if(state=='Absence'):
                    absence='1'
                    absence_count=absence_count+1
                deduct_value=deduct_in_value+deduct_out_value +one_log + absence_absence


            deduct_value_count=deduct_value_count+deduct_value



            comment=''
            hr_attendance_ids=self.pool.get('hr.attendance').search(cr,uid,[('employee_id', '=', employee_id), ('day','=',day) ,('action','=','sign_in'),]  )
            if(len(hr_attendance_ids)>0):
                attendance_data=self.pool.get('hr.attendance').browse(cr, uid, hr_attendance_ids[0], context=context)
                comment0=attendance_data.comment
                if(comment0):
                    comment= comment0.encode('utf8')
                else:
                    comment=''
                a=''



            data.append({
                        'name_employee':name_employee,
                        'name_day': name_day,
                        'day': day,
                        'description': description,
                        'project_name': str(project_name),
                        'time_in':  time_in_str ,
                        'time_out':  time_out_str ,
                        'work_time':str(work_time),#
                        'state': str(state),
                        'absence': absence,#
                        'deduct_in': deduct_in,#
                        'deduct_out': deduct_out,#
                        'deduct_value':str(deduct_value),
                        'penalty':penalty,#
                        'meal':meal,#
                        'overnight':overnight,#
                        'overtime':overtime,#
                        'excus':excus,#
                        'holiday':holiday,
                        'comment':comment,



                    })

        a=''
        #4 absence_count=0
        #holiday 13
        #5 overnight_count=0
        #6 excus_count=0
        #7 meal_count=0
        #8 penalty_count=0
        #9 overtime_count=0.0
        #10 deduct_in_count=0.0
        #11 deduct_out_count=0.0
        #12 work_time_mints_count=0
        w1=int (work_time_mints_count/60)
        w2= work_time_mints_count - (w1*60)
        wwwd=''
        if(w2<10):
            wwwd='0'
        work_time_count=str(w1)+':'+wwwd+str(w2)


        mydata.insert(4,str(absence_count))
        mydata.insert(5,str(overnight_count))
        mydata.insert(6,str(excus_count))
        mydata.insert(7,str(meal_count))
        mydata.insert(8,str(penalty_count))
        mydata.insert(9,str(overtime_count))
        mydata.insert(10,str(deduct_in_count))
        mydata.insert(11,str(deduct_out_count))
        mydata.insert(12,str(work_time_count))
        mydata.insert(13,str(holiday_count))
        mydata.insert(14,str(deduct_value_count))



        mydata.insert(0,data)
        # data[0]=  employee_id
        # data['form'].update(self.read(cr, uid, ids, ['initial_balance', 'amount_currency'])[0])
        return self.pool['report'].get_action(cr, uid, [], 'cbpo_hr_attend_new.report_attendance2_1', data=mydata, context=context)

    def print_report_attend2_done(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow(cr, uid, ids, 'quotation_sent')
        return self.pool['report'].get_action(cr, uid, ids, 'cbpo_hr_attend_new.report_attendance2_1', context=context)

    def absence_compute(self,cr,uid,ids=None,context=None):
        wizareds = self.browse(cr, uid, ids,context=None)
        wizared = wizareds[0]

        mydate = datetime.now()
        day_from_str=str(wizared.day_from)
        day_to_str=str(wizared.day_to)

        day_from =  datetime.strptime(day_from_str, "%Y-%m-%d")
        day_to =  datetime.strptime(day_to_str, "%Y-%m-%d")
        # mydatetime2 = mydatetime+  relativedelta(hours=delay)


        year=int(wizared.year)
        month=int(wizared.month)
        month_zero=''
        day_zero=''
        # if(month<10):
        #     month_zero='0'
        #
        # if(day<10):
        #     day_zero='0'
        # my_day=  str(year)+'-'+month_zero+str(month)+'-'+day_zero+str(day)

        last_day=calendar.monthrange(year, month)[1]
        end_date = date(year,month,last_day)
        start_date = date(year,month,1)
        # s1=start_date.strftime("%Y-%m-%d")
        # s2=end_date.strftime("%Y-%m-%d")
        my=str(wizared.year)+'-'+str(wizared.month)
        s3=mydate.strftime("%Y-%m-%d %H:%M:%S")
        s4=str(wizared.year)+'-'+str(wizared.month)

        company_ids=self.pool.get('res.users').read(cr, uid, uid, ["company_id"])
        cmmppny=company_ids['company_id'][0]


        company_data=self.pool.get('res.company').read(cr, uid, cmmppny, ["deduct_absence_per_day","deduct_one_in_or_out_per_day","additional_overtime_maximum","additional_overtime","additional_overtime_value","start_day","tt_in","tt_out"])
        mystartday=int(company_data['start_day'])
        tt_in=int(company_data['tt_in'])
        tt_out=int(company_data['tt_out'])


        overtime2=company_data['additional_overtime']
        overtime2_value=company_data['additional_overtime_value']
        overtime2_max=company_data['additional_overtime_maximum']

        deduct_absence_per_day=company_data['deduct_absence_per_day']
        deduct_one_in_or_out_per_day=company_data['deduct_one_in_or_out_per_day']

        y=int(wizared.year)
        m=int(wizared.month)
        m1=0
        y1=0


        if(mystartday>1):

            mystartdayend=mystartday+1
            myendday0=str(mystartdayend)
            mystartday0=str(company_data['start_day'])


            if(m>1):
                m1=m-1
            else:
                m1=1
                y1=y-1

            s1=str(y)+'-'+str(m1)+'-'+myendday0

            day_s1=y*10000+m1*100+int(myendday0)
            s2=str(y)+'-'+str(m)+'-'+mystartday0

            day_s2=y*10000+m*100+int(mystartday0)
        else:
            m1=m
            s1=str(y)+'-'+str(m1)+'-1'
            day_s1=y*10000+m1*100+int(1)
            s2=str(y)+'-'+str(m)+'-'+str(last_day)
            day_s2=y*10000+m*100+int(last_day)



        array_absence=range(1,32)
        for nnnn in range(0, 31):
            array_absence[nnnn]=''

        if(mystartday>1): # new date
            mystartdayend=mystartday-1
            myendday0=str(mystartdayend)
            mystartday0=str(company_data['start_day'])
            y=int(wizared.year)
            m=int(wizared.month)




            if(m>1):
                m1=m-1
                y1= y
            else:
                m1=1
                y1= y -1

            xx27=int(mystartday0)-1
            xx31 = int(calendar.monthrange(y1, m1)[1])
            yy1=1
            yy28=int(mystartday0)
            for x in range(xx27, xx31):
                m1_zero=''
                if(m1<10):
                    m1_zero='0'
                x_zero=''
                if(x<10):
                    x_zero='0'
                array_absence[x-1]=str(y1)+'-'+m1_zero+str(m1)+'-'+x_zero+str(x)




            for xx in range(yy1, yy28):
                m_zero=''
                if(m<10):
                    m_zero='0'
                xx_zero=''
                if(xx<10):
                    xx_zero='0'
                array_absence[xx-1]= str(y)+'-'+m_zero+str(m)+'-'+xx_zero+str(xx)




            s2=str(y)+'-'+str(m1)+'-'+myendday0

            day_s2=y*10000+m*100+int(myendday0)
            s1=str(y)+'-'+str(m)+'-'+mystartday0

            day_s1=y*10000+m1*100+int(mystartday0)
        else:
            m1=m
            s1=str(y1)+'-'+str(m1)+'-1'
            day_s1=y1*10000+m1*100+int(1)

            s2=str(y)+'-'+str(m)+'-'+str(last_day)
            day_s2=y*10000+m*100+int(last_day)


        #start code
        # for date_absence in array_absence:
        #     a=''



        date_absence=day_from.strftime('%Y-%m-%d')


        stay_in_days=True
        diff_days_ok=False
        if(day_to >= day_from):
            diff_days_ok=True



        while(stay_in_days and diff_days_ok):
            this_date_absence=  datetime.strptime(date_absence, "%Y-%m-%d")
            date_name=date_absence+' 01:01:01'
            employee_ids=self.pool.get('hr.employee').search(cr,uid,[('active' , '=' , True)]  )

            if(len(employee_ids)>0):

                for employee_id in employee_ids:
                    attendance2_ids=self.pool.get('hr.attendance2').search(cr,uid,[('employee_id' , '=' , employee_id),('day','=',date_absence)]  )
                    if(len(attendance2_ids)>0):
                        a=''
                        row_data_one_attend2 = self.pool.get('hr.attendance2').read(cr, uid, [attendance2_ids[0]],[ 'state'])
                        state=row_data_one_attend2[0]['state']
                        if(state=='in' or state=='out'):
                            o=''
                            absence=deduct_absence_per_day
                            one_log=deduct_one_in_or_out_per_day
                            self.pool.get('hr.attendance2').write(cr, uid, [attendance2_ids[0]], {'absence':'0','one_log':str(one_log)   }, context)

                        if(len(attendance2_ids)==0):
                            c='one data in hr2'
                        elif(len(attendance2_ids)>1):
                            b='more one data in hr2'

                        # the employee have attend in this day
                    else:
                        b=''
                        print('date_absence='+str(date_absence) + ' _ employee_id='+str(employee_id))
                        if(employee_id>0 and date_absence ):

                            name=str(date_absence)+' 00:00:00'
                            arr_date_abs=date_absence.split('-');
                            dayint=int(arr_date_abs[0])*10000+ int(arr_date_abs[1])*100+ int(arr_date_abs[2])
                            #doing any thing when employee is absence

                            absence=deduct_absence_per_day
                            one_log=deduct_one_in_or_out_per_day

                            #end doing
                            date_absence_time =  datetime.strptime(date_absence, "%Y-%m-%d")
                            date_absence_number=int(date_absence_time.strftime('%w'))
                            if(date_absence_number==0):

                                date_absence_number_odoo=str(6)
                            else:
                               date_absence_number_odoo=  str(date_absence_number-1)
                            add=False
                            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)  ] )
                            if(len(employee_ids)>0):
                                data_contract= self.pool.get('hr.contract').browse(cr, uid, employee_ids[0], context=context)
                                # row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours','working_hour'])
                                lenthdata1=len(data_contract)
                                if(lenthdata1>0):
                                    working_hours=data_contract.working_hours.id
                                    # day_hours=row_data_contract[0]['working_hour']
                                    calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',date_absence_number_odoo)] , context=context)
                                    if(len(calendar_ids)>0):
                                        row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])
                                        lenthdata2=len(row_data_calendar)
                                        if(lenthdata2>0):

                                            hour_from =   row_data_calendar[0]['hour_from']
                                            hour_to   =  row_data_calendar[0]['hour_to']
                                            dayofweek   =  row_data_calendar[0]['dayofweek']
                                            add=True
                            if(add):
                                self.pool.get('hr.attendance2').create(cr,uid,{'employee_id':employee_id,'absence':str(absence),'name':date_name , 'dayint':dayint, 'action':'Absence' ,'day':date_absence , 'state':'Absence' , 'action':'Absence'   })
            # end while
            end=''
            # get next day
            if(date_absence==day_to_str and diff_days_ok):
                stay_in_days=False
            next_day=  this_date_absence+  relativedelta(days=1)
            date_absence=next_day.strftime('%Y-%m-%d')

        a=''













    def delay_compute(self,cr,uid,ids=None,context=None):
        wizareds = self.browse(cr, uid, ids,context=None)
        wizared = wizareds[0]


        delay=int(wizared.delay)
        data_ids=self.pool.get('hr.fingerprint_data').search(cr,uid,[('compute' , '=' , '0')] ,order='fid')

        if(len(data_ids)>0):
            for dataID in data_ids:
                row_data_fingerprint = self.pool.get('hr.fingerprint_data').read(cr, uid, dataID,['name','fid','action'])
                lenthdata1=len(row_data_fingerprint)
                if(lenthdata1>0):
                    # fid =   row_data_fingerprint['fid']
                    name = row_data_fingerprint['name']
                    if(name):
                    # ac=row_data_fingerprint['action']
                        delay2=delay+2
                        mydatetime =  datetime.strptime(name, "%Y-%m-%d %H:%M:%S")
                        mydatetime2 = mydatetime+  relativedelta(hours=delay)
                        self.pool.get('hr.fingerprint_data').write(cr, uid, dataID, {'name': str(mydatetime2)}, context)

    def attend_set_data(self,cr,uid,ids=None,context=None):

        wizareds = self.browse(cr, uid, ids,context=None)
        wizared = wizareds[0]


        delay=int(wizared.delay)
        delay2=delay+2
        data_ids=self.pool.get('hr.fingerprint_data').search(cr,uid,[('compute' , '=' , '0')] ,order='fid')
        if(len(data_ids)>0):
            for dataID in data_ids:
                row_data_fingerprint = self.pool.get('hr.fingerprint_data').read(cr, uid, dataID,['name','fid','action'])
                lenthdata1=len(row_data_fingerprint)
                if(lenthdata1>0):
                    fid =   row_data_fingerprint['fid']
                    name = row_data_fingerprint['name']
                    ac=row_data_fingerprint['action']
                    if(name and ac):
                        # raise osv.except_osv('Date Show!', 'row_data_fingerprint : ' + str(row_data_fingerprint))
                        fmt="%Y-%m-%d %H:%M:%S"

                        mydatetime =   datetime.strptime(name, "%Y-%m-%d %H:%M:%S")
                        myfinaldate = mydatetime+  relativedelta(hours=delay)

                        # raise osv.except_osv('Date Show!', 'name : ' + name+'\n name2 : '+name2)
                        # mydate_name = datetime.strptime(name, fmt)
                        # mydate=mydate_name -  timedelta(hours=-2)
                        # myfinaldate=mydate.strftime("%Y-%m-%d %H:%M:%S")


                        actiontype =  str( row_data_fingerprint['action'])

                        fpids=self.pool.get('hr.employee').search(cr,uid,[('cbpo_fingerPrintId'  , '=' , fid)],order=None)
                        if(len(fpids)>0):
                            userid=fpids[0]
                            if actiontype == "I":
                                action = "sign_in"

                            else:
                                action = "sign_out"


                            self.pool.get('hr.attendance').create(cr,uid,{'employee_id':userid, 'name':str(myfinaldate), 'action':action ,'compute':'0'})
            self.pool.get('hr.fingerprint_data').write(cr, uid, data_ids, {'compute': '1'}, context)

    def attend_month_compute(self,cr,uid,ids=None,context=None):
        wizareds = self.browse(cr, uid, ids,context=None)
        wizared = wizareds[0]

        mydate = datetime.now()

        year=int(wizared.year)
        month=int(wizared.month)
        last_day=calendar.monthrange(year, month)[1]
        end_date = date(year,month,last_day)
        start_date = date(year,month,1)
        # s1=start_date.strftime("%Y-%m-%d")
        # s2=end_date.strftime("%Y-%m-%d")
        my=str(wizared.year)+'-'+str(wizared.month)
        s3=mydate.strftime("%Y-%m-%d %H:%M:%S")
        s4=str(wizared.year)+'-'+str(wizared.month)

        company_ids=self.pool.get('res.users').read(cr, uid, uid, ["company_id"])
        cmmppny=company_ids['company_id'][0]


        company_data=self.pool.get('res.company').read(cr, uid, cmmppny, ["additional_overtime_maximum","additional_overtime","additional_overtime_value","start_day","tt_in","tt_out"])
        mystartday=int(company_data['start_day'])
        tt_in=int(company_data['tt_in'])
        tt_out=int(company_data['tt_out'])


        overtime2=company_data['additional_overtime']
        overtime2_value=company_data['additional_overtime_value']
        overtime2_max=company_data['additional_overtime_maximum']

        y=int(wizared.year)
        m=int(wizared.month)
        m1=0
        y1=0
        aaa2=0


        if(mystartday>1): # new date
            mystartdayend=mystartday-1
            myendday0=str(mystartdayend)
            mystartday0=str(company_data['start_day'])
            y=int(wizared.year)
            m=int(wizared.month)

            if(m>1):
                m1=m-1
                y1= y
            else:
                m1=1
                y1= y -1

            s2=str(y)+'-'+str(m1)+'-'+myendday0

            day_s2=y*10000+m*100+int(myendday0)
            s1=str(y)+'-'+str(m)+'-'+mystartday0

            day_s1=y*10000+m1*100+int(mystartday0)
        else:
            m1=m
            s1=str(y1)+'-'+str(m1)+'-1'
            day_s1=y1*10000+m1*100+int(1)
            s2=str(y)+'-'+str(m)+'-'+str(last_day)
            day_s2=y*10000+m*100+int(last_day)



        # raise osv.except_osv('company ',  '\n s1:'+s1+'\n s2:'+s2)






        conn_ids=self.pool.get('hr.contract').search(cr,uid,[('month_discip' , '!=' , s4)  ] )
        if(len(conn_ids)>0):
            self.pool.get('hr.contract').write(cr, uid, conn_ids, {'allowance_count':'0','excuse_count':'0','meal_count':'0','absence_count':'0','one_log_count':'0','penalties_count':'0','overnight_count':'0','month_overtime':'0','month_discip_in': '0','days_discip_in':'0','lastupdate':str(s3) ,'month_discip':str(s4) }, context)
            # self.pool.get('hr.contract').write(cr, uid, conn_ids, {'allowance_count':'0' }, context)
            ennnnd=''

        # att3_ids=self.pool.get('hr.attendance3').search(cr,uid,[('month' , '=' , s4) ] ,order='month')
        # self.pool.get('hr.attendance3').write(cr, uid, conn_ids, {'total_discip_in': '0.00','lastupdate':s3 ,'month':s4 }, context)



        myList=  []
        ds1=datetime.strptime(s1,"%Y-%m-%d")
        ds2=datetime.strptime(s2,"%Y-%m-%d")
        attend2_ids=self.pool.get('hr.attendance2').search(cr,uid,[('dayint' , '>=' , day_s1),('dayint' , '<=' , day_s2)  ],order='employee_id asc' )
        aa1=len(attend2_ids)


        # ,('action','=','sign_in_out')

        nn=len(attend2_ids)
        aaa=str(len(attend2_ids))
        # raise osv.except_osv('attendance2 ',  '\n Total:'+aaa+'\n s1:'+s1+'\n s2:'+s2
        # +'\n Ds1:'+str(ds1)+'\n Ds2:'+str(ds2)
        # +'\n day_s1_s:'+str(day_s1)+'\n day_s2_s:'+str(day_s2))


        array_emp=[]

        if(nn>0):

            for attendID in attend2_ids:

                row_data_attend2 = self.pool.get('hr.attendance2').read(cr, uid, [attendID],['absence','one_log', 'allowance_data','overnight','meal','excus_data','discip_in','overtime_out','discip_out','employee_id','day'])

                emp_id=str(row_data_attend2[0]['employee_id'][0])


                if(emp_id not in array_emp):
                    array_emp.insert(-1, emp_id)

        myid=0
        mylastid=0
        mysum=0
        mysum_over=0
        disc=0
        mysum_disc_days=0


        disc_days=0
        last_over=0
        last_dis_day=0
        last_dis=0
        last_id=0
        last_s4=0
        last_s3=0

        meal_count=0
        absence_count=0.0
        one_log_count=0.0
        penalties_count=0.0

        allowance_count=0
        overnight_count=0
        excuse_count=0


        overtime_out_count=0
        disc=0
        disc_days=0


        aaa3=len(array_emp)
        for my_emp_id in array_emp:
            attend2_my_emp_ids=self.pool.get('hr.attendance2').search(cr,uid,[('dayint' , '>=' , day_s1),('dayint' , '<=' , day_s2) ,('employee_id','=',int(my_emp_id)) ],order='employee_id asc' )
            for attendID_Emp in attend2_my_emp_ids:
                data_attend_my_emp_and_one_month= self.pool.get('hr.attendance2').read(cr, uid, [attendID_Emp],['penalty','absence','one_log', 'allowance_data','overnight','meal','excus_data','discip_in','overtime_out','discip_out','employee_id','day'])
                absence=data_attend_my_emp_and_one_month[0]['absence']
                one_log=data_attend_my_emp_and_one_month[0]['one_log']
                penalty=data_attend_my_emp_and_one_month[0]['penalty']
                allowance_data=data_attend_my_emp_and_one_month[0]['allowance_data']
                overnight=data_attend_my_emp_and_one_month[0]['overnight']
                meal=data_attend_my_emp_and_one_month[0]['meal']
                excus_data=data_attend_my_emp_and_one_month[0]['excus_data']
                discip_in=str(data_attend_my_emp_and_one_month[0]['discip_in'])
                overtime_out=data_attend_my_emp_and_one_month[0]['overtime_out']
                discip_out=str(data_attend_my_emp_and_one_month[0]['discip_out'])
                employee_id=data_attend_my_emp_and_one_month[0]['employee_id']
                day=data_attend_my_emp_and_one_month[0]['day']

                aaa2=aaa2+1

                disc_days_in=0
                disc0_in=0
                disc_days_out=0
                disc0_out=0
                over0=0
                if(data_attend_my_emp_and_one_month[0]['discip_in'] and data_attend_my_emp_and_one_month[0]['discip_in']!='' and data_attend_my_emp_and_one_month[0]['discip_in']!=' '):

                    if(discip_in and discip_in.find('Day')==-1):
                        disc0_in=float(discip_in)

                        disc_days_in=0
                    else:

                        dayaaaa=discip_in.split('Day');
                        disc_days_in=float(dayaaaa[0])
                        # compute day from leaves here
                        disc0_in=0

                else:
                    disc0_in=0
                    disc_days_in=0


                if(data_attend_my_emp_and_one_month[0]['discip_out'] and data_attend_my_emp_and_one_month[0]['discip_out']!='' and data_attend_my_emp_and_one_month[0]['discip_out']!=' '):

                    if(discip_out   and discip_out.find('Day')==-1):
                        disc0_out=float( discip_out )

                        disc_days_out=0
                    else:

                        dayaaaa=discip_out.split('Day');
                        disc_days_out=float(dayaaaa[0])
                        # compute day from leaves here
                        disc0_out=0

                else:
                    disc0_out=0
                    disc_days_out=0


                disc=disc0_in+disc0_out
                disc_days=disc_days_in+disc_days_out

                if(data_attend_my_emp_and_one_month[0]['overtime_out'] and data_attend_my_emp_and_one_month[0]['overtime_out']!='' and data_attend_my_emp_and_one_month[0]['overtime_out']!=' '):
                    overtime_out_count=float(overtime_out)
                else:
                    overtime_out_count=0








                if(data_attend_my_emp_and_one_month[0]['overtime_out'] and data_attend_my_emp_and_one_month[0]['overtime_out']!='' and data_attend_my_emp_and_one_month[0]['overtime_out']!=' '):
                    overtime_out_count=overtime_out_count+float(overtime_out)

                if(data_attend_my_emp_and_one_month[0]['absence'] and data_attend_my_emp_and_one_month[0]['absence']!=''):
                    absence_count=absence_count+float(absence)

                if(data_attend_my_emp_and_one_month[0]['one_log'] and data_attend_my_emp_and_one_month[0]['one_log']!=''):
                    one_log_count=one_log_count+float(one_log)

                if(data_attend_my_emp_and_one_month[0]['penalty'] and data_attend_my_emp_and_one_month[0]['penalty']!=''):
                    penalties_count=penalties_count+float(penalty)

                if(data_attend_my_emp_and_one_month[0]['overtime_out'] and data_attend_my_emp_and_one_month[0]['overtime_out']!='' and data_attend_my_emp_and_one_month[0]['overtime_out']!=' '):
                    allowance_count=allowance_count+float(overtime_out)

                if(data_attend_my_emp_and_one_month[0]['allowance_data'] and data_attend_my_emp_and_one_month[0]['allowance_data']!='' and data_attend_my_emp_and_one_month[0]['allowance_data']!=' '):
                    if(allowance_data and allowance_data!=''):
                        allowance_count=allowance_count+1

                if(data_attend_my_emp_and_one_month[0]['meal'] and data_attend_my_emp_and_one_month[0]['meal']==1   and data_attend_my_emp_and_one_month[0]['meal']!=' '):
                    if(float(meal)==1):
                        meal_count=meal_count+float(meal)

                if(data_attend_my_emp_and_one_month[0]['overnight'] and  data_attend_my_emp_and_one_month[0]['overnight']==1 and data_attend_my_emp_and_one_month[0]['overnight']!=' '):
                    if(float(overnight)==1):
                        overnight_count=overnight_count+float(overnight)

                if(data_attend_my_emp_and_one_month[0]['excus_data'] and data_attend_my_emp_and_one_month[0]['excus_data']!='' and data_attend_my_emp_and_one_month[0]['excus_data']!=' ' and data_attend_my_emp_and_one_month[0]['excus_data']!='0'):
                    excuse_count=excuse_count+float(1)




            employee_id=my_emp_id
            contract_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',int(employee_id) ) ] ,order='employee_id')

            if(len(contract_ids)>0):
                for cont_id in contract_ids:
                    self.pool.get('hr.contract').write(cr, uid, cont_id, {'allowance_count':allowance_count,'excuse_count':excuse_count,'meal_count':meal_count,'absence_count':absence_count,'penalties_count':penalties_count,'one_log_count':one_log_count,'overnight_count':overnight_count,'month_overtime': overtime_out_count ,'month_discip_in': disc ,'days_discip_in':disc_days,'lastupdate':s3 ,'month_discip':s4 }, context)

            attend3_ids=self.pool.get('hr.attendance3').search(cr,uid,[('month' , '=' , s4),('employee_id' , '=' , int(employee_id) ) ] ,order='month')
            at3len=len(attend3_ids)
            # raise osv.except_osv('Show ',  '\n total:'+str(at3len)+'\n employee_id:'+str(mylastid))
            if(at3len>0):
                self.pool.get('hr.attendance3').write(cr, uid, attend3_ids, {'allowance_count':allowance_count,'excuse_count':excuse_count,'meal_count':meal_count,'total_absence':absence_count,'total_penalties':penalties_count,'total_one_log':one_log_count,'overnight_count':overnight_count,'total_overtime': overtime_out_count ,'employee_id':employee_id,'total_discip_in': disc,'days_discip_in':disc_days, 'lastupdate':s3 ,'month':s4 }, context)
            else:
                self.pool.get('hr.attendance3').create(cr,uid,{'allowance_count':allowance_count,'excuse_count':excuse_count,'meal_count':meal_count,'total_absence':absence_count,'total_penalties':penalties_count,'total_one_log':one_log_count,'overnight_count':overnight_count,'total_overtime': overtime_out_count ,'employee_id':employee_id, 'total_discip_in':disc ,'days_discip_in':disc_days, 'month':s4  ,'lastupdate':s3   })



            meal_count=0
            if(absence_count>0):
                aaaaa=''
            absence_count=0
            one_log_count=0
            penalties_count=0

            allowance_count=0
            overnight_count=0
            excuse_count=0


            overtime_out_count=0
            disc=0
            disc_days=0





        endall=''






    #
    # def attend_month_compute_old(self,cr,uid,ids=None,context=None):
    #     wizareds = self.browse(cr, uid, ids,context=None)
    #     wizared = wizareds[0]
    #
    #     mydate = datetime.now()
    #
    #     year=int(wizared.year)
    #     month=int(wizared.month)
    #     last_day=calendar.monthrange(year, month)[1]
    #     end_date = date(year,month,last_day)
    #     start_date = date(year,month,1)
    #     # s1=start_date.strftime("%Y-%m-%d")
    #     # s2=end_date.strftime("%Y-%m-%d")
    #     my=str(wizared.year)+'-'+str(wizared.month)
    #     s3=mydate.strftime("%Y-%m-%d %H:%M:%S")
    #     s4=str(wizared.year)+'-'+str(wizared.month)
    #
    #     company_ids=self.pool.get('res.users').read(cr, uid, uid, ["company_id"])
    #     cmmppny=company_ids['company_id'][0]
    #
    #
    #     company_data=self.pool.get('res.company').read(cr, uid, cmmppny, ["additional_overtime_maximum","additional_overtime","additional_overtime_value","start_day","tt_in","tt_out"])
    #     mystartday=int(company_data['start_day'])
    #     tt_in=int(company_data['tt_in'])
    #     tt_out=int(company_data['tt_out'])
    #
    #
    #     overtime2=company_data['additional_overtime']
    #     overtime2_value=company_data['additional_overtime_value']
    #     overtime2_max=company_data['additional_overtime_maximum']
    #
    #     y=int(wizared.year)
    #     m=int(wizared.month)
    #     m1=0
    #     y1=0
    #
    #
    #     if(mystartday>1): # new date
    #         mystartdayend=mystartday-1
    #         myendday0=str(mystartdayend)
    #         mystartday0=str(company_data['start_day'])
    #         y=int(wizared.year)
    #         m=int(wizared.month)
    #
    #         if(m>1):
    #             m1=m-1
    #             y1= y
    #         else:
    #             m1=1
    #             y1= y -1
    #
    #         s2=str(y)+'-'+str(m1)+'-'+myendday0
    #
    #         day_s2=y*10000+m*100+int(myendday0)
    #         s1=str(y)+'-'+str(m)+'-'+mystartday0
    #
    #         day_s1=y*10000+m1*100+int(mystartday0)
    #     else:
    #         m1=m
    #         s1=str(y1)+'-'+str(m1)+'-1'
    #         day_s1=y1*10000+m1*100+int(1)
    #         s2=str(y)+'-'+str(m)+'-'+str(last_day)
    #         day_s2=y*10000+m*100+int(last_day)
    #
    #
    #
    #     # raise osv.except_osv('company ',  '\n s1:'+s1+'\n s2:'+s2)
    #
    #
    #
    #
    #
    #
    #     conn_ids=self.pool.get('hr.contract').search(cr,uid,[('month_discip' , '!=' , s4)  ] )
    #     if(len(conn_ids)>0):
    #         self.pool.get('hr.contract').write(cr, uid, conn_ids, {'allowance_count':'0','excuse_count':'0','meal_count':'0','absence_count':'0',  'penalties_count':'0','one_log_count':'0','overnight_count':'0','month_overtime':'0','month_discip_in': '0','days_discip_in':'0','lastupdate':str(s3) ,'month_discip':str(s4) }, context)
    #         # self.pool.get('hr.contract').write(cr, uid, conn_ids, {'allowance_count':'0' }, context)
    #         ennnnd=''
    #
    #     # att3_ids=self.pool.get('hr.attendance3').search(cr,uid,[('month' , '=' , s4) ] ,order='month')
    #     # self.pool.get('hr.attendance3').write(cr, uid, conn_ids, {'total_discip_in': '0.00','lastupdate':s3 ,'month':s4 }, context)
    #
    #
    #
    #     myList=  []
    #     ds1=datetime.strptime(s1,"%Y-%m-%d")
    #     ds2=datetime.strptime(s2,"%Y-%m-%d")
    #     attend2_ids=self.pool.get('hr.attendance2').search(cr,uid,[('dayint' , '>=' , day_s1),('dayint' , '<=' , day_s2)  ],order='employee_id asc' )
    #     # ,('action','=','sign_in_out')
    #
    #     nn=len(attend2_ids)
    #     aaa=str(len(attend2_ids))
    #     # raise osv.except_osv('attendance2 ',  '\n Total:'+aaa+'\n s1:'+s1+'\n s2:'+s2
    #     # +'\n Ds1:'+str(ds1)+'\n Ds2:'+str(ds2)
    #     # +'\n day_s1_s:'+str(day_s1)+'\n day_s2_s:'+str(day_s2))
    #     myid=0
    #     mylastid=0
    #     mysum=0
    #     mysum_over=0
    #     disc=0
    #     mysum_disc_days=0
    #
    #
    #     disc_days=0
    #     last_over=0
    #     last_dis_day=0
    #     last_dis=0
    #     last_id=0
    #     last_s4=0
    #     last_s3=0
    #
    #     meal_count=0
    #     absence_count=0
    #     one_log_count=0
    #
    #     allowance_count=0
    #     overnight_count=0
    #     excuse_count=0
    #     array_emp=[]
    #
    #     if(nn>0):
    #
    #         for attendID in attend2_ids:
    #
    #             disc0=0
    #             disc1=0
    #             over0=0
    #             disc=0
    #             disc0_in=0
    #             disc1_out=0
    #             disc_days=0
    #             disc_days_in=0
    #             disc_days_out=0
    #
    #
    #
    #             row_data_attend2 = self.pool.get('hr.attendance2').read(cr, uid, [attendID],['absence','one_log', 'allowance_data','overnight','meal','excus_data','discip_in','overtime_out','discip_out','employee_id','day'])
    #
    #             emp_id=str(row_data_attend2[0]['employee_id'][0])
    #             array_emp.insert(-1, emp_id)
    #
    #             if(row_data_attend2[0]['discip_in'] or row_data_attend2[0]['discip_out']):
    #                 disc00=str(row_data_attend2[0]['discip_in'])
    #                 disc000=str(row_data_attend2[0]['discip_out'])
    #                 absence= row_data_attend2[0]['absence']
    #                 one_log= row_data_attend2[0]['absence']
    #                 if(absence>0):
    #                     aaa=''
    #
    #
    #
    #
    #
    #
    #
    #                 if(row_data_attend2[0]['discip_in']):
    #                     if(disc00 and disc00.find('Day')==-1):
    #                         disc0_in=float(row_data_attend2[0]['discip_in'])
    #                         day=False
    #                         disc_days_in=0
    #                     else:
    #                         day=True
    #                         dayaaaa=disc00.split('Day');
    #                         disc_days_in=float(dayaaaa[0])
    #                         # compute day from leaves here
    #                         disc0_in=0
    #                 else:
    #                     disc0=0
    #                     disc_days_in=0
    #
    #                 if(disc000 and disc000!='' and disc000!=' '):
    #                     if(disc000 and disc000.find('Day')==-1):
    #                         discip_outdiscip_out=row_data_attend2[0]['discip_out']
    #                         disc1_out=float(row_data_attend2[0]['discip_out'])
    #                         day=False
    #                         disc_days_out=0
    #                     else:
    #                         day=True
    #                         dayaaaa2=disc000.split('Day');
    #                         disc_days_out=float(dayaaaa2[0])
    #                         # compute day from leaves here
    #                         disc1_out=0
    #
    #                 else:
    #                     disc1_out=0
    #                     disc_days_out=0
    #
    #
    #
    #
    #
    #             if(row_data_attend2[0]['overtime_out'] and row_data_attend2[0]['overtime_out']!='' and row_data_attend2[0]['overtime_out']!=' '):
    #                 over0=float(row_data_attend2[0]['overtime_out'])
    #             else:
    #                 over0=0
    #
    #
    #
    #             myid0=str(row_data_attend2[0]['employee_id'][0])
    #
    #             disc=disc0_in+disc1_out
    #             disc_days=disc_days_in+disc_days_out
    #             myid=int(row_data_attend2[0]['employee_id'][0])
    #             last_over=over0
    #             last_dis_day=disc_days
    #             last_dis=disc
    #             last_id=myid
    #
    #
    #
    #
    #             if(mylastid!=0):
    #                 if(mylastid==myid):
    #
    #                     mysum=mysum+disc
    #                     mysum_over=mysum_over+float(over0)
    #                     mysum_disc_days=mysum_disc_days+disc_days
    #
    #                     absence_count==absence_count+row_data_attend2[0]['absence']
    #                     one_log_count==one_log_count+row_data_attend2[0]['one_log']
    #
    #                     if(row_data_attend2[0]['allowance_data']!='' and row_data_attend2[0]['allowance_data']!='0'):
    #                         allowance_count=allowance_count+1
    #
    #                     if(row_data_attend2[0]['meal']==1  ):
    #                         meal_count=meal_count+1
    #
    #                     if(row_data_attend2[0]['overnight']==1):
    #                         overnight_count=overnight_count+1
    #
    #                     if(row_data_attend2[0]['excus_data']!='' and row_data_attend2[0]['excus_data']!='0'):
    #                         excuse_count=excuse_count+1
    #
    #
    #
    #
    #                 else:
    #
    #                     contract_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',mylastid) ] ,order='employee_id')
    #
    #                     if(len(contract_ids)>0):
    #
    #                         mycomp=-1;
    #                         row_data_contract = self.pool.get('hr.contract').read(cr, uid, contract_ids[0],['working_hour'])
    #                         working_hour =  float( row_data_contract['working_hour'])
    #                         mycomp0=float(mysum)/float(100)
    #                         mycomp1=float(working_hour)
    #                         # mycomp= mycomp0  * working_hour
    #                         mycomp= float(mysum)
    #                         myover=float(mysum_over)
    #
    #                         # if(row_data_attend2[0]['allowance_data']!=''):
    #                         #     allowance_count=allowance_count+1
    #                         #
    #                         # if(row_data_attend2[0]['meal']!=''):
    #                         #     meal_count=meal_count+1
    #                         #
    #                         # if(row_data_attend2[0]['overnight']!=''):
    #                         #     overnight_count=overnight_count+1
    #                         #
    #                         # if(row_data_attend2[0]['excus_data']!=''):
    #                         #     excuse_count=excuse_count+1
    #
    #
    #                         # contract_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',mylastid) ] ,order='employee_id')
    #
    #                         self.pool.get('hr.contract').write(cr, uid, contract_ids[0], {'allowance_count':allowance_count,'excuse_count':excuse_count,'meal_count':meal_count,'absence_count':absence_count,'one_log_count':one_log_count,'overnight_count':overnight_count,'month_overtime': mysum_over ,'month_discip_in': mysum ,'days_discip_in':mysum_disc_days,'lastupdate':s3 ,'month_discip':s4 }, context)
    #
    #                         attend3_ids=self.pool.get('hr.attendance3').search(cr,uid,[('month' , '=' , s4),('employee_id' , '=' , mylastid) ] ,order='month')
    #                         at3len=len(attend3_ids)
    #                         # raise osv.except_osv('Show ',  '\n total:'+str(at3len)+'\n employee_id:'+str(mylastid))
    #                         if(at3len>0):
    #                             self.pool.get('hr.attendance3').write(cr, uid, attend3_ids, {'allowance_count':allowance_count,'excuse_count':excuse_count,'meal_count':meal_count,'absence_count':absence_count,'one_log_count':one_log_count,'overnight_count':overnight_count,'total_overtime': mysum_over ,'total_discip_in': mysum,'days_discip_in':mysum_disc_days, 'lastupdate':s3 ,'month':s4 }, context)
    #                         else:
    #                             self.pool.get('hr.attendance3').create(cr,uid,{'allowance_count':allowance_count,'excuse_count':excuse_count,'meal_count':meal_count,'absence_count':absence_count,'one_log_count':one_log_count,'overnight_count':overnight_count,'total_overtime': mysum_over ,'employee_id':mylastid, 'total_discip_in':mysum ,'days_discip_in':mysum_disc_days, 'month':s4  ,'lastupdate':s3   })
    #























































    #                         mylastid=myid
    #                         mysum=0
    #                         mysum_over=0
    #                         mysum_disc_days=0
    #
    #                         allowance_count=0
    #
    #                         meal_count=0
    #                         absence_count=0
    #                         one_log_count=0
    #
    #                         overnight_count=0
    #
    #                         excuse_count=0
    #
    #                     #raise osv.except_osv('OOO ',  '\n '+str(contract_ids[0])+'\n'+str(last_total_disc))
    #                     #raise osv.except_osv('Msg nooooooot ',  '\n last_total_disc \n '+str(last_total_disc)+'\n ID='+myid0+'\n mylastID='+str(mylastid))
    #
    #
    #             else:
    #                 mylastid=myid
    #                 mysum=mysum+disc
    #                 mysum_over=mysum_over+float(over0)
    #                 mysum_disc_days=mysum_disc_days+disc_days
    #
    #                 absence_count==absence_count+row_data_attend2[0]['absence']
    #                 one_log_count==one_log_count+row_data_attend2[0]['one_log']
    #                 if(row_data_attend2[0]['allowance_data']!='' and row_data_attend2[0]['allowance_data']!='0'):
    #                     allowance_count=allowance_count+1
    #
    #                 if(row_data_attend2[0]['meal']==1 ):
    #                     meal_count=meal_count+1
    #
    #                 if(row_data_attend2[0]['overnight']==1 ):
    #                     overnight_count=overnight_count+1
    #
    #                 if(row_data_attend2[0]['excus_data']!='' and row_data_attend2[0]['excus_data']!='0'):
    #                     excuse_count=excuse_count+1
    #
    #
    #         end=''
    #         #
    #         # last_over
    #         #         last_dis_day
    #         #         last_dis
    #         #         last_id
    #         contract_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',last_id) ] ,order='employee_id')
    #
    #         if(len(contract_ids)>0):
    #
    #             self.pool.get('hr.contract').write(cr, uid, contract_ids[0], {'allowance_count':allowance_count,'excuse_count':excuse_count,'meal_count':meal_count,'absence_count':absence_count,'one_log_count':one_log_count,'overnight_count':overnight_count,'month_overtime': mysum_over ,'month_discip_in': mysum ,'days_discip_in':mysum_disc_days,'lastupdate':s3 ,'month_discip':s4 }, context)
    #
    #         attend3_ids=self.pool.get('hr.attendance3').search(cr,uid,[('month' , '=' , s4),('employee_id' , '=' , last_id) ] ,order='month')
    #         at3len=len(attend3_ids)
    #         # raise osv.except_osv('Show ',  '\n total:'+str(at3len)+'\n employee_id:'+str(mylastid))
    #         if(at3len>0):
    #             self.pool.get('hr.attendance3').write(cr, uid, attend3_ids, {'allowance_count':allowance_count,'excuse_count':excuse_count,'meal_count':meal_count,'absence_count':absence_count,'one_log_count':one_log_count,'overnight_count':overnight_count,'total_overtime': mysum_over ,'total_discip_in': mysum,'days_discip_in':mysum_disc_days, 'lastupdate':s3 ,'month':s4 }, context)
    #         else:
    #             if(last_id>0):
    #                 self.pool.get('hr.attendance3').create(cr,uid,{'allowance_count':allowance_count,'excuse_count':excuse_count,'meal_count':meal_count,'absence_count':absence_count,'one_log_count':one_log_count,'overnight_count':overnight_count,'total_overtime': mysum_over ,'employee_id':last_id, 'total_discip_in':mysum ,'days_discip_in':mysum_disc_days, 'month':s4  ,'lastupdate':s3   })
    #
    #
    #             # contract_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',mylastid) ] ,order='employee_id')
    #             # self.pool.get('hr.contract').write(cr, uid, contract_ids[0], {'month_discip_in': mysum ,'lastupdate':s3 }, context)
    #
    #             #raise osv.except_osv('Msg nooooooot ',  '\n Msg \n '+str(total_disc)+'\n ID='+myid0)
    #
    #
    #         #raise osv.except_osv('ALL DATA',  '\n Start : '+s1+'\n End : '+s2+'\n Date : '+s3+'\n ALl Employee : '+aaa)


    def update_attend_compute(self,cr,uid,ids=None,context=None):
        wizareds = self.browse(cr, uid, ids,context=None)
        wizared = wizareds[0]

        mydate =  datetime.now()

        year=int(wizared.year)
        month=int(wizared.month)
        last_day=calendar.monthrange(year, month)[1]
        end_date = date(year,month,last_day)
        start_date = date(year,month,1)
        # s1=start_date.strftime("%Y-%m-%d")
        # s2=end_date.strftime("%Y-%m-%d")
        my=str(wizared.year)+'-'+str(wizared.month)
        s3=mydate.strftime("%Y-%m-%d %H:%M:%S")
        s4=str(wizared.year)+'-'+str(wizared.month)

        company_ids=self.pool.get('res.users').read(cr, uid, uid, ["company_id"])
        cmmppny=company_ids['company_id'][0]








        company_data=self.pool.get('res.company').read(cr, uid, cmmppny, ["maximum_deduction_day","hours_have_meal","additional_overtime_value_holiday","additional_overtime_maximum","additional_overtime","additional_overtime_value","start_day","tt_in","tt_out"])
        mystartday=int(company_data['start_day'])
        tt_in=int(company_data['tt_in'])
        tt_out=int(company_data['tt_out'])
        overtime2=company_data['additional_overtime']
        overtime2_value=company_data['additional_overtime_value']
        overtime2_max=company_data['additional_overtime_maximum']
        overtime2_value_holiday=company_data['additional_overtime_value_holiday']
        overtime2_hours_have_meal=company_data['hours_have_meal']
        maximum_deduction_day=float(company_data['maximum_deduction_day'])


        y=int(wizared.year)
        m=int(wizared.month)
        m1=0
        y1=0
        if(m>1):
            m1=m-1
        else:
            m1=1
            y1=y-1

        if(mystartday>1):
            mystartdayend=mystartday+1
            myendday0=str(mystartdayend)
            mystartday0=str(company_data['start_day'])
            y=int(wizared.year)
            m=int(wizared.month)



            s1=str(y)+'-'+str(m1)+'-'+myendday0

            day_s1=y*10000+m1*100+int(myendday0)
            s2=str(y)+'-'+str(m)+'-'+mystartday0

            day_s2=y*10000+m*100+int(mystartday0)
        else:
            m1=m
            s1=str(y)+'-'+str(m1)+'-1'
            day_s1=y*10000+m1*100+int(1)
            s2=str(y)+'-'+str(m)+str(last_day)
            day_s2=y*10000+m*100+int(last_day)
        # ADD Absence TO  ALL contract RECORDS
        if(mystartday>1): # new date
            mystartdayend=mystartday-1
            myendday0=str(mystartdayend)
            mystartday0=str(company_data['start_day'])
            y=int(wizared.year)
            m=int(wizared.month)

            if(m>1):
                m1=m-1
                y1= y
            else:
                m1=1
                y1= y -1

            s2=str(y)+'-'+str(m1)+'-'+myendday0

            day_s2=y*10000+m*100+int(myendday0)
            s1=str(y)+'-'+str(m)+'-'+mystartday0

            day_s1=y*10000+m1*100+int(mystartday0)
        else:
            m1=m
            s1=str(y1)+'-'+str(m1)+'-1'
            day_s1=y1*10000+m1*100+int(1)
            s2=str(y)+'-'+str(m)+'-'+str(last_day)
            day_s2=y*10000+m*100+int(last_day)



        # END Absence

        attend2_ids=self.pool.get('hr.attendance2').search(cr,uid,[('dayint' , '>=' , day_s1),('dayint' , '<=' , day_s2) ,('action','=','sign_in_out')],order='time_in asc')
        nn=len(attend2_ids)
        aaa=str(len(attend2_ids))
        # raise osv.except_osv('attendance2 ',  '\n Total:'+aaa+'\n s1:'+s1+'\n s2:'+s2
        # +'\n Ds1:'+str(ds1)+'\n Ds2:'+str(ds2)
        # +'\n day_s1_s:'+str(day_s1)+'\n day_s2_s:'+str(day_s2))

        arr_count=range(0,1000000)
        for x in arr_count:
            arr_count[x]=0

        arr_count2=range(0,1000000)
        for x2 in arr_count2:
            arr_count2[x2]=0

        arr_count3=range(0,1000000)
        for x3 in arr_count3:
            arr_count3[x3]=0

        arr_count4=range(0,1000000)
        for x4 in arr_count4:
            arr_count4[x4]=0

        arr_count5=range(0,1000000)
        for x5 in arr_count5:
            arr_count5[x5]=0

        arr_count6=range(0,1000000)
        for x6 in arr_count6:
            arr_count6[x6]=0


        arr_count66=range(0,1000000)
        for x66 in arr_count66:
            arr_count66[x66]=0

        arr_count7=range(0,1000000)
        for x7 in arr_count7:
            arr_count7[x7]=0


        desss='0'
        desss2='0'

        if(nn>0):
            myid=0
            mylastid=0
            mysum=0
            disc=0
            disc_days=0
            hour_from=0
            for attendID in attend2_ids:


                row_data_attend2 = self.pool.get('hr.attendance2').read(cr, uid, [attendID],['schedule_time_in','schedule_time_out','time_in','time_out','name','discip_in','discip_out','employee_id','day'])
                discip_in=str(row_data_attend2[0]['discip_in'])
                employee_id=int(row_data_attend2[0]['employee_id'][0])

                day=str(row_data_attend2[0]['day'])
                arr_str_day=day.split("-")
                daynow=0
                if(len(arr_str_day)>0 ):
                    daynow=int(arr_str_day[0])*10000+int(arr_str_day[1])*100+int(arr_str_day[2])



                time_in=row_data_attend2[0]['time_in']
                # time_in_aaaa=row_data_attend2[0]['time_in']

                if(time_in):
                    time_in_date=datetime.strptime(time_in,'%Y-%m-%d %H:%M:%S')

                    numberofdate_int=int(time_in_date.strftime('%w'))


                    if(numberofdate_int==0 ):
                        numberofdate=str(6)
                    else:
                        numberofdate=str(numberofdate_int-1)

                    # numberofdate=str(numberofdate_int)

                    print('my numberofdate_int  = '+str(numberofdate_int)
                    +' \n numberofdate = '+numberofdate
                    +' \n Date = ' +str(time_in_date))


                    hour_to=0
                    hour_from=0
                     # --------------- get working hours -------------
                    employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
                    if(len(employee_ids)>0):
                        row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours','working_hour'])
                        lenthdata1=len(row_data_contract)
                        if(lenthdata1>0):
                            working_hours=row_data_contract[0]['working_hours'][0]
                            day_hours=row_data_contract[0]['working_hour']
                            calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                            if(len(calendar_ids)>0):
                                row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])
                                lenthdata2=len(row_data_calendar)
                                if(lenthdata2>0):
                                    hour_from =   row_data_calendar[0]['hour_from']
                                    hour_to   =  row_data_calendar[0]['hour_to']
                                    dayofweek   =  row_data_calendar[0]['dayofweek']

                                    # raise osv.except_osv('numberofdate','numberofdate='+str(numberofdate)
                                    # +'\n date='+str(time_in_date)
                                    #  +'\n dayofweek='+str(dayofweek))


                     # --------------- end get working hours -------------
                    day=str(row_data_attend2[0]['day'])

                    schedule_time_in=float(hour_from)
                    schedule_time_in_0=int(schedule_time_in)
                    schedule_time_in_1=int((float(schedule_time_in_0)-float(schedule_time_in))*60)
                    s_time_in=schedule_time_in_0*60+schedule_time_in_1


                    schedule_time_out=float(hour_to)
                    schedule_time_out_0=int(schedule_time_out)
                    schedule_time_out_1=int((float(schedule_time_out_0)-float(schedule_time_out))*60)
                    s_time_out=schedule_time_out_0*60+schedule_time_out_1

                    my_time=0

                    if(time_in and time_in.find(':')!=-1):
                        time_in_arr0=time_in.split(' ');
                        time_in_arr=time_in_arr0[1].split(':');
                        time_h=time_in_arr[0]
                        time_m=time_in_arr[1]

                        my_time_in=(int(time_h)+tt_in)*60 +int(time_m)
                        diff_in=my_time_in-s_time_in
                        a=''
                    if(diff_in>0):
                        # late in
                        desss='0'
                        mydissid=0
                        count_dis_id=0
                        dis_id=0
                        diff_in_str=''
                        discipline_ids_count=0

                        #aa
                        employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
                        if(len(employee_ids)>0):
                            row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours','working_hour'])
                            lenthdata1=len(row_data_contract)
                            if(lenthdata1>0):
                                working_hours=row_data_contract[0]['working_hours'][0]
                                day_hours=row_data_contract[0]['working_hour']
                        else:
                            working_hours=0
                        allowance_time_to=0
                        allowance_ids=self.pool.get('hr.allowance').search(cr,uid,[('calendar_id' , '=' , working_hours)  ,('daytype' , '=','late_in')] , context=context)
                        if(len(allowance_ids)>0):
                            row_data_allowance = self.pool.get('hr.allowance').read(cr, uid, [allowance_ids[0]],['id','tt_from','tt_to','repetition','name'])
                            allowance_time_to   =  row_data_allowance[0]['tt_to']
                            allowance_time_from   =  row_data_allowance[0]['tt_from']
                            allowance_repetition   =  row_data_allowance[0]['repetition']
                            allowance_name   =  row_data_allowance[0]['name']
                            allowance_id   =  row_data_allowance[0]['id']

                            ea=int(str(employee_id)+str(allowance_id))

                            allowance_used=arr_count5[ea]

                        #aa
                        else:
                            allowance_repetition=0
                            allowance_time_from=0
                            allowance_time_to=0
                            allowance_used=0

                        # if(daynow==20150712):
                    # raise osv.except_osv('daynow!', 'daynow =  '+str(daynow))
                        excus_data='0'
                        excuse_ids=self.pool.get('hr.excuse').search(cr,uid,[('employee_id' , '=' , employee_id),('state' , '=','Approved'),('type' , '=','Excuse') ,('daytype' , '=','late_in'),('day_excuse' , '=',daynow)] , context=context)
                        if(len(excuse_ids)>0):
                            row_data_excuse = self.pool.get('hr.excuse').read(cr, uid, [excuse_ids[0]],['name','time_excuse'])
                            time_excuse=int(row_data_excuse[0]['time_excuse'])
                            print('time_excuse  = '+str(time_excuse))
                            name_excuse=row_data_excuse[0]['name']
                            excuse_used=arr_count6[employee_id]




                        else:
                            time_excuse=0
                            excuse_used=0
                            name_excuse=''


                        if( time_excuse>0 ):
                            a='have ex'
                            arr_count6[employee_id]=excuse_used+1
                            # print('Have Excuse ')
                            diff_in=diff_in-time_excuse
                            excus_data='('+str(excuse_used)+') '+str(time_excuse)+' Mints'
                        else:
                            excus_data='0'




                        # start mission

                        mission_ids=self.pool.get('hr.excuse').search(cr,uid,[('employee_id' , '=' , employee_id),('state' , '=','Approved'),('type' , '=','Mission') ,('daytype' , '=','late_in'),('day_excuse' , '=',daynow)] , context=context)
                        if(len(mission_ids)>0):
                            row_data_mission = self.pool.get('hr.excuse').read(cr, uid, [mission_ids[0]],['name','time_excuse'])
                            time_mission=int(row_data_mission[0]['time_excuse'])
                            print('time_mission  = '+str(time_mission))
                            mission_used=arr_count66[employee_id]

                        else:
                            time_mission=0
                            mission_used=0
                            name_excuse=''


                        if( time_mission>0 ):
                            a='have mission'
                            arr_count66[employee_id]=mission_used+1
                            # print('Have Excuse ')
                            diff_in=diff_in-time_mission
                            mission_data='('+str(mission_used)+') '+str(time_mission)+' Mints'
                        else:
                            mission_data='0'


                        # end mission

                        if(diff_in>=allowance_time_from and  diff_in<=allowance_time_to and allowance_used < allowance_repetition ):


                            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
                            if(len(employee_ids)>0):
                                discipline_ids=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours),('daytype','=','late_in')] ,order='t_from')
                                discipline_ids_count=len(discipline_ids)
                            if(discipline_ids_count>0):
                                for discipline_id in discipline_ids:
                                    row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id,['id','name','deductype','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','l3','l4'])
                                    t_from=row_data_discipline['t_from']
                                    t_to=row_data_discipline['t_to']

                                    if( t_from<diff_in and t_to>=diff_in ):
                                        mydissid=row_data_discipline['name']
                                        em=int(str(employee_id)+str(mydissid))
                                        dis_id=row_data_discipline['id']
                                        nnnn=arr_count[em]
                                        nnnn1=nnnn+1
                                        # arr_count[em]=nnnn1
                                        count_dis_id=arr_count[em]
                                        desss='0'


                            diff_in_time_all=float(diff_in)/float(60)
                            diff_in_time_int=int(diff_in_time_all)
                            diff_in_time_kaser=(float( diff_in_time_all ) - float(diff_in_time_int))*60
                            diff_in_time_kaser_int=int(diff_in_time_kaser)

                            if(diff_in_time_int<10):
                                n1='0'
                            else:
                                n1=''

                            if(diff_in_time_kaser_int<10):
                                n2='0'
                            else:
                                n2=''
                            diff_in_str='L|'+n1+str(diff_in_time_int)+':'+n2+str(diff_in_time_kaser_int)

                            print('Allowance Repetition Now Used No.: '+str(allowance_used+1))
                            arr_count5[ea]=allowance_used+1
                            allowance_data='('+str(allowance_used+1)+')'
                            self.pool.get('hr.attendance2').write(cr, uid, [attendID], {'schedule_time_in':str(hour_from),'schedule_time_out':str(hour_to),'mission_data':mission_data, 'excus_data':excus_data, 'mission_data2':'','allowance_data':allowance_data,'compute': '1' ,'discip_in':'0','discip_in_id_count':'0','discip_in_id':'0' ,'diff_time_in':diff_in_str  }, context)
                            a_in='' # Late in
                        else:

                            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
                            if(len(employee_ids)>0):
                                discipline_ids=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours),('daytype','=','late_in')] ,order='t_from')
                                discipline_ids_count=len(discipline_ids)
                            if(discipline_ids_count>0):
                                for discipline_id in discipline_ids:
                                    row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id,['id','name','deductype','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','l3','l4'])
                                    t_from=row_data_discipline['t_from']
                                    t_to=row_data_discipline['t_to']

                                    if( t_from<diff_in and t_to>=diff_in ):
                                        mydissid=row_data_discipline['name']
                                        em=int(str(employee_id)+str(mydissid))
                                        dis_id=row_data_discipline['id']
                                        nnnn=arr_count[em]
                                        nnnn1=nnnn+1
                                        arr_count[em]=nnnn1
                                        count_dis_id=arr_count[em]
                                        desss='0'


                                        diff_in_time_all=float(diff_in)/float(60)
                                        diff_in_time_int=int(diff_in_time_all)
                                        diff_in_time_kaser=(float( diff_in_time_all ) - float(diff_in_time_int))*60
                                        diff_in_time_kaser_int=int(diff_in_time_kaser)

                                        if(diff_in_time_int<10):
                                            n1='0'
                                        else:
                                            n1=''

                                        if(diff_in_time_kaser_int<10):
                                            n2='0'
                                        else:
                                            n2=''
                                        diff_in_str='L|'+n1+str(diff_in_time_int)+':'+n2+str(diff_in_time_kaser_int)


                                        l1=row_data_discipline['l1']
                                        l2=row_data_discipline['l2']
                                        l3=row_data_discipline['l3']
                                        l4=row_data_discipline['l4']
                                        if(count_dis_id==1 and desss=='0'):
                                            if(row_data_discipline['deductype']=='Hours'):

                                                desss=float(row_data_discipline['d1'])
                                            else:

                                                desss=(float(row_data_discipline['d1'])*float(day_hours))/float(100)

                                            if(l1!=0):
                                                desss=str(l1)+'Day'
                                        elif(count_dis_id==2 and desss=='0'):
                                            if(row_data_discipline['deductype']=='Hours'):

                                                desss=float(row_data_discipline['d2'])
                                            else:

                                                desss=(float(row_data_discipline['d2'])*float(day_hours))/float(100)
                                            if(l2!=0):
                                                desss=str(l2)+'Day'
                                        elif(count_dis_id==3 and desss=='0'):
                                            if(row_data_discipline['deductype']=='Hours'):

                                                desss=float(row_data_discipline['d3'])
                                            else:

                                                desss=(float(row_data_discipline['d3'])*float(day_hours))/float(100)
                                            if(l3!=0):
                                                desss=str(l3)+'Day'
                                        elif(count_dis_id>3 and desss=='0'):
                                            if(row_data_discipline['deductype']=='Hours'):

                                                desss=float(row_data_discipline['d4'])
                                            else:
                                                desss=(float(row_data_discipline['d4'])*float(day_hours))/float(100)
                                            if(l4!=0):
                                                desss=str(l4)+'Day'
                                        desss=str(desss)


                             # if this day agazaaa in come
                            if(s_time_in==0 and s_time_out==0):

                                desss=''
                                count_dis_id=0
                                mydissid=0
                                excus_data='0'
                                mission_data=''
                                diff_in_str='holiday'
                                # raise osv.except_osv('numberofdate','numberofdate='+str(numberofdate))

                            print('employee_id:'+str(employee_id)+' _ discip_in:'+desss+' _ discip_in_id_count:'+str(count_dis_id)+' _ discip_in_id:'+str(mydissid))
                            self.pool.get('hr.attendance2').write(cr, uid, [attendID], {'schedule_time_in':str(hour_from),'schedule_time_out':str(hour_to),'mission_data':mission_data, 'excus_data':excus_data,'allowance_data':'','compute': '1' ,'discip_in':desss,'discip_in_id_count':count_dis_id,'discip_in_id':mydissid ,'diff_time_in':diff_in_str }, context)
                            a_in='' # Late in
                    elif(diff_in==0):
                        #  come in time


                        b=''
                    else:
                        #  early in
                        diff_in=abs(diff_in)
                        a_in='E|'+str(diff_in)
                        diff_in_time_all=float(diff_in)/float(60)
                        diff_in_time_int=int(diff_in_time_all)
                        diff_in_time_kaser=(float( diff_in_time_all ) - float(diff_in_time_int))*60
                        diff_in_time_kaser_int=int(diff_in_time_kaser)

                        if(diff_in_time_int<10):
                            n1='0'
                        else:
                            n1=''

                        if(diff_in_time_kaser_int<10):
                            n2='0'
                        else:
                            n2=''
                        diff_in_str='E|'+n1+str(diff_in_time_int)+':'+n2+str(diff_in_time_kaser_int)
                        self.pool.get('hr.attendance2').write(cr, uid, [attendID], { 'schedule_time_in':str(hour_from),'schedule_time_out':str(hour_to),'compute': '1' ,   'diff_time_in':diff_in_str }, context)

                        employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
                        if(len(employee_ids)>0):
                            discipline_ids=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours),('daytype','=','early_in')] ,order='t_from')
                            discipline_ids_count=len(discipline_ids)
                            if(discipline_ids_count>0):
                                for discipline_id in discipline_ids:
                                    row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id,['id','name','deductype','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','l3','l4'])
                                    t_from=row_data_discipline['t_from']
                                    t_to=row_data_discipline['t_to']

                                    if( t_from<diff_in and t_to>=diff_in ):
                                        mydissid=row_data_discipline['name']
                                        em7=int(str(employee_id)+str(mydissid))
                                        dis_id=row_data_discipline['id']
                                        nnnn=arr_count7[em7]
                                        nnnn1=nnnn+1
                                        arr_count[em7]=nnnn1
                                        count_dis_id=arr_count[em7]
                                        desss='0'



                                        l1=row_data_discipline['l1']
                                        l2=row_data_discipline['l2']
                                        l3=row_data_discipline['l3']
                                        l4=row_data_discipline['l4']
                                        if(count_dis_id==1 and desss=='0'):
                                            if(row_data_discipline['deductype']=='Hours'):

                                                desss=float(row_data_discipline['d1'])
                                            else:

                                                desss=(float(row_data_discipline['d1'])*float(day_hours))/float(100)

                                            if(l1!=0):
                                                desss=str(l1)+'Day'
                                        elif(count_dis_id==2 and desss=='0'):
                                            if(row_data_discipline['deductype']=='Hours'):

                                                desss=float(row_data_discipline['d2'])
                                            else:

                                                desss=(float(row_data_discipline['d2'])*float(day_hours))/float(100)
                                            if(l2!=0):
                                                desss=str(l2)+'Day'
                                        elif(count_dis_id==3 and desss=='0'):
                                            if(row_data_discipline['deductype']=='Hours'):

                                                desss=float(row_data_discipline['d3'])
                                            else:

                                                desss=(float(row_data_discipline['d3'])*float(day_hours))/float(100)
                                            if(l3!=0):
                                                desss=str(l3)+'Day'
                                        elif(count_dis_id>3 and desss=='0'):
                                            if(row_data_discipline['deductype']=='Hours'):

                                                desss=float(row_data_discipline['d4'])
                                            else:
                                                desss=(float(row_data_discipline['d4'])*float(day_hours))/float(100)
                                            if(l4!=0):
                                                desss=str(l4)+'Day'
                                        desss=str(desss)
                                        des_in=float(desss)

                                        if(des_in>= maximum_deduction_day):
                                            desss=str(maximum_deduction_day)



                                        self.pool.get('hr.attendance2').write(cr, uid, [attendID], {'schedule_time_in':str(hour_from),'schedule_time_out':str(hour_to), 'compute': '1' ,'discip_in':desss,'discip_in_id_count':count_dis_id,'discip_in_id':mydissid ,'diff_time_in':diff_in_str }, context)







                        c=''




                # end  in


                # start   out
                time_out=row_data_attend2[0]['time_out']
                time_in=row_data_attend2[0]['time_in']

                if(time_out):
                    time_out_date=datetime.strptime(time_out,'%Y-%m-%d %H:%M:%S')
                    numberofdate=time_out_date.strftime('%w')
                    numberofdate_int=int(time_out_date.strftime('%w'))
                    if(numberofdate_int==0 ):
                        numberofdate=str(6)
                    else:
                        numberofdate=str(numberofdate_int-1)


                        # raise osv.except_osv('numberofdate','numberofdate='+str(numberofdate)
                        # +'\n date='+str(time_in_date)
                        # +'\n NOOOOO')


                    # nameaa.weekday()
                    hour_from=0
                    hour_to=0
                    day_hours=0
                    allow_overtime_first_weekend=False
                    allow_overtime_second_weekend=False
                    overtime_first_weekend=0
                    overtime_second_weekend=0
                    first_weekend_more_working_time=False
                    second_weekend_more_working_time=False

                     # --------------- get working hours -------------
                    employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
                    if(len(employee_ids)>0):
                        row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours','working_hour','first_weekend' ,'second_weekend','allow_overtime_first_weekend','allow_overtime_second_weekend','overtime_first_weekend','overtime_second_weekend','second_weekend_more_working_time','first_weekend_more_working_time'])
                        lenthdata1=len(row_data_contract)
                        if(lenthdata1>0):
                            working_hours=row_data_contract[0]['working_hours'][0]
                            day_hours=row_data_contract[0]['working_hour']
                            first_weekend=row_data_contract[0]['first_weekend']
                            second_weekend=row_data_contract[0]['second_weekend']
                            allow_overtime_first_weekend=row_data_contract[0]['allow_overtime_first_weekend']
                            allow_overtime_second_weekend=row_data_contract[0]['allow_overtime_second_weekend']
                            overtime_first_weekend=row_data_contract[0]['overtime_first_weekend']
                            overtime_second_weekend=row_data_contract[0]['overtime_second_weekend']
                            first_weekend_more_working_time=row_data_contract[0]['first_weekend_more_working_time']
                            second_weekend_more_working_time=row_data_contract[0]['second_weekend_more_working_time']




                            calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                            if(len(calendar_ids)>0):
                                row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])
                                lenthdata2=len(row_data_calendar)
                                if(lenthdata2>0):
                                    hour_from =   row_data_calendar[0]['hour_from']
                                    hour_to   =  row_data_calendar[0]['hour_to']
                     # --------------- end get working hours -------------
                    day=str(row_data_attend2[0]['day'])

                    schedule_time_out=float(hour_to)
                    schedule_time_out_0=int(schedule_time_out)
                    schedule_time_out_1=int((float(schedule_time_out_0)-float(schedule_time_out))*60)
                    s_time_out=schedule_time_out_0*60+schedule_time_out_1

                    schedule_time_in=float(hour_from)
                    schedule_time_in_0=int(schedule_time_in)
                    schedule_time_in_1=int((float(schedule_time_in_0)-float(schedule_time_in))*60)
                    s_time_in=schedule_time_in_0*60+schedule_time_in_1
                    my_time=0
                    myday_out_arr=day.split('-');

                    myday_int=int(myday_out_arr[0]+myday_out_arr[1]+myday_out_arr[2])

                    day_int=0
                    day_in_int=0
                    day_out_int=0
                    zyada_yom_h=0
                    zyada_in_out=0
                    if(time_in and  time_in.find(':')!=-1):
                        time_in_arr0=time_in.split(' ');
                        time_in_arr=time_in_arr0[1].split(':');
                        time_h_in=int(time_in_arr[0])+tt_in
                        time_m_in=int(time_in_arr[1])
                        day_in_arr=time_in_arr0[0].split('-');

                        day_in_int=int(str(day_in_arr[0])+str(day_in_arr[1])+str(day_in_arr[2]))
                        daysec_in=int( int(day_in_arr[2])*24*60  +int(time_in_arr[0])*60+int(time_in_arr[1]))
                        a=''
                    if(time_out and time_out.find(':')!=-1):

                        time_out_arr0=time_out.split(' ');
                        time_out_arr=time_out_arr0[1].split(':');


                        day_out_arr=time_out_arr0[0].split('-');

                        daysec_out=int( int(day_out_arr[2])*24*60  +int(time_out_arr[0])*60+int(time_out_arr[1]))
                        day_out_int=int(str(day_out_arr[0])+str(day_out_arr[1])+str(day_out_arr[2]))

                        day_diff_in_out_int=day_out_int-day_in_int
                        zyada_in_out=daysec_out-daysec_in
                        if(day_diff_in_out_int>0):
                            zyada_yom_h=day_diff_in_out_int*24

                        time_h=int(time_out_arr[0])+tt_out +zyada_yom_h
                        time_m=int(time_out_arr[1])

                        if(time_h>=24):
                            d_y=day_out_arr[0]
                            d_m=day_out_arr[1]
                            time_h=time_h-24
                            d_d=str(int(day_out_arr[2]))
                            d_d_int=int(d_d)
                            if(d_d_int<=9):
                                d_d='0'+d_d
                        else:
                            d_y=day_out_arr[0]
                            d_m=day_out_arr[1]
                            d_d=day_out_arr[2]


                        diff_out=0
                        diff_in=0


                        day_int=int(d_y+d_m+d_d)

                        my_time_out=int(time_h)*60 +int(time_m)
                        my_time_in=int(time_h_in)*60 +int(time_m_in)

                        # my_time_in=(int(time_h_in)+tt_in)*60 +int(time_m_in)

                        # raise osv.except_osv('myday!', 'myday : ' + str(myday_int)+ ' \n '+
                        # ' Time ='+str(time_out)+"\n"+
                        #                      ' day : ' +str(day_int) +'\n'
                        # +'Time now ='+str(my_time_out))

                        if(myday_int==day_int):
                            # my_time_out=(int(time_h)+tt_out)*60 +int(time_m)
                            my_time_out=(int(time_h))*60 +int(time_m)
                            diff_out=my_time_out-s_time_out
                            # raise osv.except_osv('نفس التاريخ', 'my_time_out : ' +str(my_time_out))
                        elif(myday_int<day_int):
                            my_time_out=(int(time_h))*60 +int(time_m)
                            diff_out=my_time_out+(1440-s_time_out)


                            # raise osv.except_osv('مش نفسو!', 'my_time_out : ' +str(my_time_out)
                            # +'\n s_time_out='+str(s_time_out)
                            # +'\n diff_out='+str(diff_out))

                            aa=''
                        else:
                            aa=''
                            # raise osv.except_osv(' ولا اي كلام ', ' ولا اي كلام : ' )

                        a=''
                    if(diff_out<0):
                        # Early Out
                        desss2='0'
                        diff_out=abs(diff_out)
                        mydissid2=0
                        count_dis_id2=0
                        dis_id2=0
                        diff_out_str2=''
                        discipline_ids2_count=0
                        employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
                        if(len(employee_ids)>0):
                            row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours','working_hour'])
                            lenthdata1=len(row_data_contract)
                        if(lenthdata1>0):
                            working_hours=row_data_contract[0]['working_hours'][0]

                            discipline_ids2=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours),('daytype','=','early_out')] ,order='t_from')
                            discipline_ids2_count=len(discipline_ids2)

                        excuse_ids=self.pool.get('hr.excuse').search(cr,uid,[('employee_id' , '=' , employee_id),('state' , '=','Approved'),('type' , '=','Excuse') ,('daytype' , '=','early_out'),('day_excuse' , '=',daynow)] , context=context)
                        if(len(excuse_ids)>0):
                            row_data_excuse = self.pool.get('hr.excuse').read(cr, uid, [excuse_ids[0]],['name','time_excuse'])
                            time_excuse=int(row_data_excuse[0]['time_excuse'])
                            print('time_excuse  = '+str(time_excuse))
                            name_excuse=row_data_excuse[0]['name']
                            excuse_used=arr_count6[employee_id]




                        else:
                            time_excuse=0
                            excuse_used=0
                            name_excuse=''


                        if( time_excuse>0 ):
                            a='have ex'
                            arr_count6[employee_id]=excuse_used+1
                            # print('Have Excuse ')
                            diff_out=diff_out-time_excuse
                            excus_data2='('+str(excuse_used)+') '+str(time_excuse)+' Mints'
                        else:
                            excus_data2='0'


                        mission_ids=self.pool.get('hr.excuse').search(cr,uid,[('employee_id' , '=' , employee_id),('state' , '=','Approved'),('type' , '=','Mission') ,('daytype' , '=','early_out'),('day_excuse' , '=',daynow)] , context=context)
                        if(len(mission_ids)>0):
                            row_data_mission = self.pool.get('hr.excuse').read(cr, uid, [mission_ids[0]],['name','time_excuse'])
                            time_mission=int(row_data_mission[0]['time_excuse'])
                            print('time_mission  = '+str(time_mission))
                            name_mission=row_data_mission[0]['name']
                            mission_used=arr_count66[employee_id]




                        else:
                            time_mission=0
                            mission_used=0
                            mission_data2=''
                            name_excuse=''

                        mission_data2=''
                        if( time_mission>0 ):
                            a='have mission'
                            arr_count66[employee_id]=mission_used+1
                            # print('Have Excuse ')
                            diff_out=diff_out-time_mission
                            mission_data2='('+str(mission_used)+') '+str(time_mission)+' Mints'
                        else:
                            mission_data2=''


                        if(discipline_ids2_count>0):
                            for discipline_id2 in discipline_ids2:
                                row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id2,['id','name','deductype','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','l3','l4'])
                                t_from=row_data_discipline['t_from']
                                t_to=row_data_discipline['t_to']

                                if( t_from<diff_out and t_to>=diff_out ):
                                    mydissid2=row_data_discipline['name']
                                    em2=int(str(employee_id)+str(mydissid2))
                                    dis_id=row_data_discipline['id']
                                    nnnnx=arr_count2[em2]
                                    nnnn1x=nnnnx+1
                                    arr_count2[em2]=nnnn1x
                                    count_dis_id2=arr_count2[em2]
                                    desss2='0'




                                    diff_out_time_all=float(diff_out)/float(60)
                                    diff_out_time_int=int(diff_out_time_all)
                                    diff_out_time_kaser=(float( diff_out_time_all ) - float(diff_out_time_int))*60
                                    diff_out_time_kaser_int=int(diff_out_time_kaser)

                                    if(diff_out_time_int<10):
                                        n1='0'
                                    else:
                                        n1=''

                                    if(diff_out_time_kaser_int<10):
                                        n2='0'
                                    else:
                                        n2=''
                                    diff_out_str2='E|'+n1+str(diff_out_time_int)+':'+n2+str(diff_out_time_kaser_int)






                                    l1=row_data_discipline['l1']
                                    l2=row_data_discipline['l2']
                                    l3=row_data_discipline['l3']
                                    l4=row_data_discipline['l4']
                                    if(count_dis_id2==1 and desss2=='0'):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss2=float(row_data_discipline['d1'])
                                        else:
                                            desss2=(float(row_data_discipline['d1'])*float(day_hours))/float(100)

                                        if(l1!=0):
                                            desss2=str(l1)+'Day'
                                    elif(count_dis_id2==2 and desss2=='0'):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss2=float(row_data_discipline['d2'])
                                        else:

                                            desss2=(float(row_data_discipline['d2'])*float(day_hours))/float(100)
                                        if(l2!=0):
                                            desss2=str(l2)+'Day'
                                    elif(count_dis_id2==3 and desss2=='0'):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss2=float(row_data_discipline['d3'])
                                        else:
                                            desss2=(float(row_data_discipline['d3'])*float(day_hours))/float(100)
                                        if(l3!=0):
                                            desss2=str(l3)+'Day'
                                    elif(count_dis_id2>3 and desss2=='0'):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss2=float(row_data_discipline['d4'])
                                        else:
                                            desss2=(float(row_data_discipline['d4'])*float(day_hours))/float(100)

                                        if(l4!=0):
                                            desss2=str(l4)+'Day'


                                    desss2=str(desss2)


                        company_ids=self.pool.get('res.users').read(cr, uid, uid, ["company_id"])
                        cmmppny=company_ids['company_id'][0]


                        company_data=self.pool.get('res.company').read(cr, uid, cmmppny, ["maximum_deduction_day","additional_overtime_maximum","additional_overtime","additional_overtime_value","start_day","tt_in","tt_out"])
                        mystartday=int(company_data['start_day'])
                        tt_in=int(company_data['tt_in'])
                        tt_out=int(company_data['tt_out'])


                        overtime2=company_data['additional_overtime']
                        overtime2_value=company_data['additional_overtime_value']
                        overtime2_max=company_data['additional_overtime_maximum']
                        maximum_deduction_day=float(company_data['maximum_deduction_day'])

                        if(desss and desss.find('Day')==-1):
                            # discip_in=float(discip_in)


                            des_in=float(desss)
                        else:
                            des_in=0
                        des_out=float(desss2)
                        des_total=des_in+des_out

                        if(des_total<= maximum_deduction_day):
                            a='Do Noting '
                            # Do Noting
                        else:
                            if(des_in>=maximum_deduction_day):
                                desss2='0'
                                c=''
                            else:
                                des_dif= maximum_deduction_day -des_in
                                if(des_dif<=des_out):

                                    e='Do Noting in out'
                                else:
                                    desss2=str(des_dif)
                                    f=''
                                d=''
                            b=''
                        print('employee_id:'+str(employee_id)+' _ discip_out:'+desss2+' _ discip_out_id_count:'+str(count_dis_id2)+' _ discip_out_id:'+str(mydissid2))
                        self.pool.get('hr.attendance2').write(cr, uid, [attendID], {'schedule_time_in':str(hour_from),'schedule_time_out':str(hour_to), 'mission_data2':mission_data2 , 'excus_data2':excus_data2, 'compute': '1' ,'overtime_out':'0','discip_out':desss2,'discip_out_id_count':count_dis_id2,'discip_out_id':mydissid2,'diff_time_out':diff_out_str2 }, context)
                        a_out='' # Early Out

                    elif(diff_out==0):
                        #  out in time

                        self.pool.get('hr.attendance2').write(cr, uid, [attendID], {'schedule_time_in':str(hour_from),'schedule_time_out':str(hour_to),'compute': '1' ,'overtime_out':'0','excus_data2':'','mission_data2':'','overtime_out_id_count':'0','overtime_out_id':'0','diff_time_out':'In Time' }, context)



                        b=''
                    else:
                         # Late Out
                        diff_out=  abs(diff_out)
                        desss3='0'
                        desss4=0
                        ds_total_str=''
                        mydissid3=0
                        count_dis_id3=0
                        dis_id3=0
                        diff_out_str3=''
                        working_hours=0
                        allow_overtime=0
                        allow_meal=0
                        desss_over=0
                        more_working_time=False
                        overtime2_value_holiday=0
                        weekenddata=''
                        have_weekend=False
                        desss4=0

                        working_hour=0

                        employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')

                        if(len(employee_ids)>0):
                            row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours','working_hour','allow_overtime','allow_meal'])
                            lenthdata1=len(row_data_contract)
                        else:
                            lenthdata1=0

                        if(lenthdata1>0):
                            working_hours=row_data_contract[0]['working_hours'][0]
                            working_hour=row_data_contract[0]['working_hour']

                            allow_overtime=row_data_contract[0]['allow_overtime']
                            allow_meal=row_data_contract[0]['allow_meal']
                        discipline_ids3=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours),('daytype','=','late_out')] ,order='t_from')
                        if(len(discipline_ids3)>0):
                            for discipline_id3 in discipline_ids3:
                                row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id3,['id','name','deductype','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','l3','l4'])
                                t_from=row_data_discipline['t_from']
                                t_to=row_data_discipline['t_to']

                                if( t_from<diff_out and t_to>=diff_out ):
                                    mydissid3=row_data_discipline['name']
                                    em3=int(str(employee_id)+str(mydissid3))
                                    dis_id=row_data_discipline['id']
                                    nnnnxo=arr_count3[em3]
                                    nnnn1xo=nnnnxo+1
                                    arr_count3[em3]=nnnn1xo
                                    count_dis_id3=arr_count3[em3]
                                    desss3=0
                                    desss4=0
                                    ds_total_str=''




                                    diff_out_time_all=float(diff_out)/float(60)
                                    diff_out_time_int=int(diff_out_time_all)
                                    diff_out_time_kaser=(float( diff_out_time_all ) - float(diff_out_time_int))*60
                                    diff_out_time_kaser_int=int(diff_out_time_kaser)

                                    if(diff_out_time_int<10):
                                        n1='0'
                                    else:
                                        n1=''
                                    if(diff_out_time_kaser_int<10):
                                        n2='0'
                                    else:
                                        n2=''
                                    diff_out_str3='L|'+n1+str(diff_out_time_int)+':'+n2+str(diff_out_time_kaser_int)



                                    l1=row_data_discipline['l1']
                                    l2=row_data_discipline['l2']
                                    l3=row_data_discipline['l3']
                                    l4=row_data_discipline['l4']

                                    desss3_str=''

                                    if(count_dis_id3==1 and desss3==0):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss3=float(row_data_discipline['d1'])
                                        else:

                                            desss3=(float(row_data_discipline['d1'])*float(day_hours))/float(100)
                                        if(l1!=0 and overtime2!=True):
                                            desss3_str=str(l1)+'Day'
                                    elif(count_dis_id3==2 and desss3==0):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss3=float(row_data_discipline['d2'])

                                        else:

                                            desss3=(float(row_data_discipline['d2'])*float(day_hours))/float(100)
                                        if(l2!=0 and overtime2!=True):
                                            desss3_str=str(l2)+'Day'
                                    elif(count_dis_id3==3 and desss3==0):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss3=float(row_data_discipline['d3'])
                                        else:
                                            desss3=(float(row_data_discipline['d3'])*float(day_hours))/float(100)
                                        if(l3!=0 and overtime2!=True):
                                            desss3_str=str(l3)+'Day'
                                    elif(count_dis_id3>3 and desss3==0):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss3=float(row_data_discipline['d4'])
                                        else:
                                            desss3=(float(row_data_discipline['d4'])*float(day_hours))/float(100)
                                        if(l4!=0 and overtime2!=True):
                                            desss3_str=str(l4)+'Day'
                        overnight=0
                        diff_in=abs( s_time_in-my_time_in)
                        day_diiff_int_hours=0
                        meal=0
                        have_weekend=False
                        overtime_out_value = 0
                        if(s_time_in==0 and s_time_out==0):

                            if(allow_overtime_first_weekend):
                                if(numberofdate==first_weekend):
                                    overtime2_value_holiday=overtime_first_weekend
                                    weekenddata='first_weekend'
                                    more_working_time=first_weekend_more_working_time
                                    have_weekend=True


                            if(allow_overtime_second_weekend):
                                if(numberofdate==second_weekend):
                                    overtime2_value_holiday=overtime_second_weekend
                                    weekenddata='second_weekend'
                                    more_working_time=second_weekend_more_working_time
                                    have_weekend=True


                            #     first_weekend=row_data_contract[0]['first_weekend']
                            # second_weekend=row_data_contract[0]['second_weekend']
                            # allow_overtime_first_weekend=row_data_contract[0]['allow_overtime_first_weekend']
                            # allow_overtime_second_weekend=row_data_contract[0]['allow_overtime_second_weekend']
                            # overtime_first_weekend=row_data_contract[0]['overtime_first_weekend']
                            # overtime_second_weekend=row_data_contract[0]['overtime_second_weekend']




                            # this code 4 T&D Work in saturday 1 hour = 1 hour over time
                            # if(numberofdate=='5'):
                            #     overtime2_value_holiday=1
                            # end code T&D


                            total_dif_in_out=(int(diff_out ) - int(diff_in))/int(60)
                            new_overtime_diff=0
                            if(more_working_time):
                                if(day_hours>total_dif_in_out):
                                    new_overtime_diff=0
                                else:

                                    new_overtime_diff=total_dif_in_out-day_hours
                                desss_over= float(new_overtime_diff)*float(overtime2_value_holiday)
                                diff_out_str3=str(new_overtime_diff)+' Hours'

                            else:
                                desss_over= float(total_dif_in_out)*float(overtime2_value_holiday)
                                diff_out_str3=str(total_dif_in_out)+' Hours'

                            # raise osv.except_osv(' Agaaaaaaaazaaaaaaa  !', '\n   diff_out='+str(diff_out)
                            #                      +'\n   diff_in='+str(diff_in)
                            #                      +'\n   s_time_out='+str(s_time_out)
                            #                      +'\n   s_time_in='+str(s_time_in)    )


                            # raise osv.except_osv(' Agaaaaaaaazaaaaaaa  !',
                            # '\n value_holiday : '+ str(total_dif_in_out))
                            # raise osv.except_osv('desss4', 'desss4='+str(total_dif_out))
                            overnight=0
                            mydissid3=0

                        else:
                        # s in and s out is not 0
                            a=''
                        #     diff_out_str3='L|'+n1+str(diff_out_time_int)+':'+n2+str(diff_out_time_kaser_int)
                        # End if this day agazaaa




                             # hashem if not week end
                            if( myday_int  ==  day_int ):
                                a=''
                                day_diiff_int_hours=0
                            else:

                                day_diiff_int_hours=24

                            total_dif_in_out=int(abs((my_time_out   - my_time_in))/float(60))

                            print("my_time_in="+str(my_time_in) +" --- my_time_out="+str(my_time_out)+" --- total_dif_in_out="+str(total_dif_in_out)

                            +"\n  --- myday_int="+str(myday_int)+" --- day_int="+str(day_int))

                            if(total_dif_in_out>=day_hours):
                                hr_over_final=int(day_diiff_int_hours)+ int(total_dif_in_out-day_hours)
                            else:
                                hr_over_final=0

                            meal=0
                            if(total_dif_in_out>=overtime2_hours_have_meal and allow_meal):
                                meal=1

                            if(overtime2 and allow_overtime):
                                # raise osv.except_osv('IAM !', 'Iam In NOW   '  )
                                a=''

                                total_dif_out=(int(diff_out)/int(60))


                                Total_over_time= int(day_diiff_int_hours) + int(float( total_dif_in_out)- float( working_hour ))
                                if( Total_over_time <=overtime2_max):
                                    aa=''

                                    # raise osv.except_osv('NOW STATE !', 'overtime2_max<=total_dif_out   '  )
                                    if(Total_over_time>0):
                                        desss4= float(Total_over_time )*float(overtime2_value)
                                    # raise osv.except_osv('Total!', 'Total_over_time : ' +str(Total_over_time) +'  overtime2_value=' +str(overtime2_value) +  " ***   day_diiff_int_hours=" +str(day_diiff_int_hours))
                                    diff_out_str3=str(Total_over_time)+' Hours'
                                    overnight=0

                                else:
                                    bb=''
                                    overnight=1

                                    # desss4=0


                                    # raise osv.except_osv('NOW STATE !', ' NOOOOOOT (overtime2_max<=total_dif_out   ) diff_out='+str(diff_out) +' _ total_dif_out='+str(total_dif_out)+' _ overtime2_max='+str(overtime2_max) )
                            else:
                                # raise osv.except_osv('IAM NOT !', 'Iam Nottttttttt In NOW   '  )
                                b=''
                                desss4=0
                            # if this day agazaaa


                            # hashem END  if not week end

                        ds_total=float(desss3)+float(desss4)+float(desss_over)
                        ds_total_str=str(ds_total)

                        # raise osv.except_osv('Total!', 'desss3 = ' +str(desss3 )+  'desss4 = ' +str(desss4 )+  'desss_over = ' +str(desss_over ))
                        # raise osv.except_osv('ds_total', 'ds_total='+str(ds_total) + '\n desss_over='+str(desss_over))

                        #
                        #  + '\n diff_in='+str(diff_out) )









                        if(overnight==1):
                            meal=1
                            # this 4 T&D
                            ds_total_str='06.0'

                              # The defulte
                         #hashem work
                        print('employee_id:'+str(employee_id)+' _ overtime_out:'+ds_total_str+' _ overtime_out_id_count:'+str(count_dis_id3 )+' _ overtime_out_id:'+str(mydissid3))
                        self.pool.get('hr.attendance2').write(cr, uid, [attendID], {'schedule_time_in':str(hour_from),'schedule_time_out':str(hour_to),'compute': '1' ,'meal':meal,'overnight':overnight,'overtime_out':ds_total_str, 'overtime_out_value':overtime2_value_holiday ,'excus_data2':'','mission_data2':'','overtime_out_id_count':count_dis_id3,'overtime_out_id':mydissid3,'diff_time_out':diff_out_str3 }, context)

                        c='' # Late Out



                    #hash#
                # else:
                    # no time in  (false)
                    x=''
        aa=''







    def attend_compute(self,cr,uid,ids=None,context=None):
        sameuser=0
        samedate=0
        a_in=''
        a_out=''
        company_ids=self.pool.get('res.users').read(cr, uid, uid, ["company_id"])
        cmmppny=company_ids['company_id'][0]


        company_data=self.pool.get('res.company').read(cr, uid, cmmppny, ["start_day","tt_in","tt_out"])
        mystartday=int(company_data['start_day'])
        tt_in=int(company_data['tt_in'])
        tt_out=int(company_data['tt_out'])



        attend_ids=self.pool.get('hr.attendance').search(cr,uid,[ ('compute', '=', '0')],order='day ASC')
        total=len(attend_ids)
        data_name=[]
        data_day=[]
        data_employee=[]
        data_action=[]
        array_day=[]
        array_employee=[]
        i=0
        j=0
        if(total>0):
            for attendID in attend_ids:
                row_data_attendance = self.pool.get('hr.attendance').read(cr, uid, [attendID],['name','action','employee_id','day','day_name','compute']) 
                id =   row_data_attendance[0]['id']
                name =   row_data_attendance[0]['name']
                day =  str( row_data_attendance[0]['day'])
                employee_id =   row_data_attendance[0]['employee_id'][0]
                action =  str( row_data_attendance[0]['action'])
                name_date=datetime.strptime(name,'%Y-%m-%d %H:%M:%S')
                numberofdate=name_date.strftime('%w')
                numberofdate_int=int(name_date.strftime('%w'))
                # if(numberofdate_int==6):
                if(numberofdate_int==0 ):
                    numberofdate=str(6)
                else:
                    numberofdate=str(numberofdate_int-1)



                data_name.insert(-1, name) 
                data_day.insert(-1, day) 
                data_employee.insert(-1, employee_id) 
                data_action.insert(-1, action) 
                        
                res_e=0
                for el_e in array_employee:
                    if(el_e==employee_id):
                        res_e=res_e+1
                if(res_e>0):
                    myres_e=False  
                else:
                    myres_e= True
                 
                if(myres_e):
                    array_employee.insert(-1, employee_id)  
                    j=j+1
                
                res=0
                for el in array_day:
                    if(el==day):
                        res=res+1
                if(res>0):
                    myres=False  
                else:
                    myres= True
                 
                if(myres):
                    array_day.insert(-1, day)  
                    i=i+1
                
                
                
                
                
        for emp_id in array_employee:
            for one_day in array_day:
                attend_in_ids=self.pool.get('hr.attendance').search(cr,uid,[('compute' , '=' , '0'),('action' , '=' , 'sign_in'),('employee_id' , '=' , emp_id),('day' , '=' , one_day)] ,order='name ASC')
                total_in=len(attend_in_ids)
                if(total_in>0):
                    row_data_in_attendance = self.pool.get('hr.attendance').read(cr, uid, [attend_in_ids[0]],['name','action','employee_id','day','day_name','compute'])
                    name_in =  str( row_data_in_attendance[0]['name'])
                    # id_in=   row_data_in_attendance[0]['id']
                    have_in=True
                else:
                    have_in=False
                    
                    
                attend_out_ids=self.pool.get('hr.attendance').search(cr,uid,[('compute' , '=' , '0'),('action' , '=' , 'sign_out'),('employee_id' , '=' , emp_id),('day' , '=' , one_day)] ,order='name DESC')
                total_out=len(attend_out_ids)
                if(total_out>0):
                    row_data_out_attendance = self.pool.get('hr.attendance').read(cr, uid, [attend_out_ids[0]],['name','action','employee_id','day','day_name','compute'])
                    name_out =  str(  row_data_out_attendance[0]['name'])
                    # id_out=   row_data_out_attendance[0]['id']
                    have_out=True
                else:
                    have_out=False


                hour_from=0
                hour_to=0
                 # --------------- get working hours -------------
                employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
                if(len(employee_ids)>0):
                    row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours','working_hour','allow_overtime','allow_meal'])
                    lenthdata1=len(row_data_contract)
                    if(lenthdata1>0):
                        working_hours=row_data_contract[0]['working_hours'][0]
                        day_hours=row_data_contract[0]['working_hour']
                        allow_overtime=row_data_contract[0]['allow_overtime']
                        allow_meal=row_data_contract[0]['allow_meal']

                        calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                        if(len(calendar_ids)>0):
                            row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])
                            lenthdata2=len(row_data_calendar)
                            if(lenthdata2>0):
                                hour_from =   row_data_calendar[0]['hour_from']
                                hour_to   =  row_data_calendar[0]['hour_to']
                 # --------------- end get working hours -------------


                schedule_time_out=float(hour_to)
                schedule_time_out_0=int(schedule_time_out)
                schedule_time_out_1=int((float(schedule_time_out_0)-float(schedule_time_out))*60)
                s_time_out=schedule_time_out_0*60+schedule_time_out_1
                my_time=0
                schedule_time_in=float(hour_from)
                schedule_time_in_0=int(schedule_time_in)
                schedule_time_in_1=int((float(schedule_time_in_0)-float(schedule_time_in))*60)
                s_time_in=schedule_time_in_0*60+schedule_time_in_1
                if(have_out):
                    time_out=name_out;
                    if(time_out and time_out.find(':')!=-1):
                        time_out_arr0=time_out.split(' ');
                        time_out_arr=time_out_arr0[1].split(':');
                        time_h=time_out_arr[0]
                        time_m=time_out_arr[1]

                        my_time_out=(int(time_h)+tt_out)*60 +int(time_m)
                        diff_out=my_time_out-s_time_out
                        a=''
                    if(diff_out<0):
                         # Early Out
                        diff_out=abs(diff_out)
                        a_out='E|'+str(diff_out)

                        diff_out_time_all=float(diff_out)/float(60)
                        diff_out_time_int=int(diff_out_time_all)
                        diff_out_time_kaser=(float( diff_out_time_all ) - float(diff_out_time_int))*60
                        diff_out_time_kaser_int=int(diff_out_time_kaser)

                        if(diff_out_time_int<10):
                            n1='0'
                        else:
                            n1=''

                        if(diff_out_time_kaser_int<10):
                            n2='0'
                        else:
                            n2=''
                        a_out='E|'+n1+str(diff_out_time_int)+':'+n2+str(diff_out_time_kaser_int)
                    elif(diff_out==0):
                        a_out='In Time'
                    else:
                         # Late Out
                        a_out='L|'+str(diff_out)
                        diff_out_time_all=float(diff_out)/float(60)
                        diff_out_time_int=int(diff_out_time_all)
                        diff_out_time_kaser=(float( diff_out_time_all ) - float(diff_out_time_int))*60
                        diff_out_time_kaser_int=int(diff_out_time_kaser)

                        if(diff_out_time_int<10):
                            n1='0'
                        else:
                            n1=''
                        if(diff_out_time_kaser_int<10):
                            n2='0'
                        else:
                            n2=''
                        a_out='L|'+n1+str(diff_out_time_int)+':'+n2+str(diff_out_time_kaser_int)






                if(have_in):
                    time_in=name_in
                    if(time_in and time_in.find(':')!=-1):
                        time_in_arr0=time_in.split(' ');
                        time_in_arr=time_in_arr0[1].split(':');
                        time_h=time_in_arr[0]
                        time_m=time_in_arr[1]

                        my_time_in=(int(time_h)+tt_in)*60 +int(time_m)
                        diff_in=my_time_in-s_time_in
                        a=''
                        if(diff_in>0):
                            # late in
                            a_in='L|'+str(diff_in)
                            diff_in_time_all=float(diff_in)/float(60)
                            diff_in_time_int=int(diff_in_time_all)
                            diff_in_time_kaser=(float( diff_in_time_all ) - float(diff_in_time_int))*60
                            diff_in_time_kaser_int=int(diff_in_time_kaser)

                            if(diff_in_time_int<10):
                                n1='0'
                            else:
                                n1=''

                            if(diff_in_time_kaser_int<10):
                                n2='0'
                            else:
                                n2=''
                            a_in='L|'+n1+str(diff_in_time_int)+':'+n2+str(diff_in_time_kaser_int)


                        elif(diff_in==0):
                            a_in='In Time'
                        else:
                             # Early in
                            diff_in=abs(diff_in)
                            a_in='E|'+str(diff_in)
                            diff_in_time_all=float(diff_in)/float(60)
                            diff_in_time_int=int(diff_in_time_all)
                            diff_in_time_kaser=(float( diff_in_time_all ) - float(diff_in_time_int))*60
                            diff_in_time_kaser_int=int(diff_in_time_kaser)

                            if(diff_in_time_int<10):
                                n1='0'
                            else:
                                n1=''

                            if(diff_in_time_kaser_int<10):
                                n2='0'
                            else:
                                n2=''
                            a_in='E|'+n1+str(diff_in_time_int)+':'+n2+str(diff_in_time_kaser_int)


                if(have_in==True and have_out==True):
                    a1=''
                    self.pool.get('hr.attendance2').create(cr,uid,{'employee_id':emp_id, 'name':name_in, 'action':'sign_in_out' ,'time_in':name_in ,'time_out':name_out , 'state':'in_out' ,'diff_time_in':a_in,'diff_time_out':a_out})
                elif(have_in==True and have_out==False):
                    self.pool.get('hr.attendance2').create(cr,uid,{'employee_id':emp_id, 'name':name_in, 'action':'sign_in_out' ,'time_in':name_in ,  'state':'in' ,'diff_time_in':a_in })
                    a2=''
                elif(have_in==False and have_out==True):
                    self.pool.get('hr.attendance2').create(cr,uid,{'employee_id':emp_id, 'name':name_out, 'action':'sign_in_out' , 'time_out':name_out , 'state':'out','diff_time_out':a_out  })
                    a3=''
                ddd=''

                # now update compute = 1 in this day from this employee_id
                date_ids=self.pool.get('hr.attendance').search(cr,uid,[('day' , '=' , one_day),('employee_id','=',emp_id) ] ,order='name DESC')
                self.pool.get('hr.attendance').write(cr, uid, date_ids, {'compute': '1'}, context)
                d=''
                
                
            e=''      
        a=array_day       
        a=''
#                 
#                 if(action=='sign_in'):
#                     
#                     attend_out_ids=self.pool.get('hr.attendance').search(cr,uid,[('compute' , '=' , '0'),('action' , '=' , 'sign_out'),('employee_id' , '=' , employee_id),('day' , '=' , day)] ,order='name DESC')
#                     total_out=len(attend_out_ids)
#                     if(total_out>0):
#                         row_data_out_attendance = self.pool.get('hr.attendance').read(cr, uid, [attend_out_ids[0]],['name','action','employee_id','day','day_name','compute']) 
#                         name_out =   row_data_out_attendance[0]['name']
#                         id_out=   row_data_out_attendance[0]['id']
#                         state='in_out'
#                         if(sameuser!=employee_id or samedate!=day):
#                             self.pool.get('hr.attendance2').create(cr,uid,{'employee_id':employee_id, 'name':name, 'action':'sign_in_out' ,'time_in':name, 'time_out':name_out, 'state':state })
#                     else:
#                         name_out=''
#                         state='in'
#                         if(sameuser!=employee_id or samedate!=day):
#                             self.pool.get('hr.attendance2').create(cr,uid,{'employee_id':employee_id, 'name':name, 'action':'sign_in_out' ,'time_in':name , 'state':state })
#                     
#                         
#                          
#                         a_end_if_and_same=''
#                 else:
#                     state='out'
#                     if(sameuser!=employee_id or samedate!=day):
#                             self.pool.get('hr.attendance2').create(cr,uid,{'employee_id':employee_id, 'name':name, 'action':'sign_in_out' ,'time_out':name , 'state':state })
#                     
#                 sameuser=employee_id
#                 samedate=day
#             date_ids=self.pool.get('hr.attendance').search(cr,uid,[('day' , '=' , day) ] ,order='name DESC')
#             self.pool.get('hr.attendance').write(cr, uid, date_ids, {'compute': '1'}, context)
#             oook=''
#                 
#                 
#             bb=''
#         aa=''
#         
        
    def in_my_array(self,cr,uid,value,array):
        res=0
        for el in array:
            if(el==value):
                res=res+1
        if(res>0):
            return True
        else:
            return False      
    def update(self,cr,uid,ids=None,context=None):
        # get values from wizared form
        # set up some constants
        wizareds = self.browse(cr, uid, ids,context=None)
        wizared = wizareds[0]
        
        if(wizared.useingconf==True): 
            idds=self.pool.get('hr.finger.conf').search(cr,uid,[('active' , '=' , 'True')] ,order='id')
            if(len(idds)>0):
                row_data = self.pool.get('hr.finger.conf').read(cr, uid, [idds[0]],['db', 'path','dbname','username','password'])
                lenthdata=len(row_data)
                if(lenthdata>0):
                    db = row_data[0]['db']
                    mdb_path = row_data[0]['path']
                    db_name = row_data[0]['dbname']
                    username = row_data[0]['username']
                    password = row_data[0]['password']
    

        else:
            
            db = wizared.db
            mdb_path = wizared.path
            db_name = wizared.dbname
            username = wizared.username
            password = wizared.password
            db = wizared.db      
        # if context is None: context = {}
# # connect to db

# #file_exists=os.path.exists(db) # check if file exists
        


        # db_path = os.path.join("path", "toyour", "/home/core/Downloads/a.mdb")
        # odbc_connection_str = 'DRIVER={MDBTools};DBQ=%s;' % (db_path)

        # connection = pyodbc.connect(odbc_connection_str)
        # cursor = connection.cursor()
        # query = "SELECT * from (select USERID , MIN([CHECKTIME]) AS lDate, CHECKTYPE from CHECKINOUT where CHECKTYPE='I' group by USERID,CHECKTYPE,Int([CHECKTIME]) UNION ALL select USERID , MAX([CHECKTIME]) AS lDate, CHECKTYPE from CHECKINOUT where CHECKTYPE='O' group by USERID,CHECKTYPE,Int([CHECKTIME]) ) ORDER BY USERID,lDate"
        # query = "SELECT * from CHECKINOUT; "
        # cursor.execute(query)
        # rows = cursor.fetchall()
# #
# #         connectionstring = 'DRIVER={%s};DBQ=%s;'%(db,mdb_path)
# #         a='/home/core/Downloads/a.mdb'
# #
# #         con = pyodbc.connect(connectionstring)
# #         cur = con.cursor()
# #
# # # run a query and get the results
# # #SQL = 'SELECT * FROM checkinout ORDER BY USERID,checktime asc;' # your query goes here
# #         SQL = "SELECT * from (select USERID , MIN([CHECKTIME]) AS lDate, CHECKTYPE from CHECKINOUT where CHECKTYPE='I' group by USERID,CHECKTYPE,Int([CHECKTIME]) UNION ALL select USERID , MAX([CHECKTIME]) AS lDate, CHECKTYPE from CHECKINOUT where CHECKTYPE='O' group by USERID,CHECKTYPE,Int([CHECKTIME]) ) ORDER BY USERID,lDate;"
# #         rows = cur.execute(SQL).fetchall()
# #         cur.close()
# #         con.close()
          
        # employee_id = 0;
        # userids = 0;
        # userid = 0;
        # time_delta_to=0
        # time_delta_from=0
        # msg=''
        # _from_time=''
        # _to_time=''
        # for r in rows:
            # if(employee_id == int(r[0])):
                # xx=0 #same user
            # else:
                # employee_id= int(r[0])
                # xx=1
                
                
            # name=r[1] #date
			# #change date format
            # name1=name.strftime("%Y-%m-%d %H:%M:%S")
            # schedule_time=name.strftime('%H:%M:%S')
            
            # schedule_time_h=int(name.strftime('%H'))
            # schedule_time_m=int(name.strftime('%M'))
            # schedule_time_s=int(name.strftime('%S'))
            
            # schedule_time_sec=schedule_time_h*60*60+schedule_time_m*60+schedule_time_s
            
            # numberofdate=name.strftime('%w')
            
            # if(numberofdate=='1'):
                # thisday='Monday'
            # elif(numberofdate=='2'):
                # thisday='Tuesday'
            # elif(numberofdate=='3'):
                # thisday='Wednesday'
            # elif(numberofdate=='4'):
                # thisday='Thursday'
            # elif(numberofdate=='5'):
                # thisday='Friday'
            # elif(numberofdate=='6'):
                # thisday='Saturday'
            # elif(numberofdate=='0'):
                # thisday='Sunday'
             
            
            # df='%Y-%m-%d %H:%M:%S'
            # cur_date1 = datetime.strptime(name1,df)
            # cur_date = datetime.strftime(cur_date1, DEFAULT_SERVER_DATETIME_FORMAT)
			
            # checktype=r[2].replace('\"','')#punch type
            
            # if checktype == "I":
              # action = "sign_in"
              # aa='in'
            # else:
              # action = "sign_out"
              # aa='out'
              
            # try:
 
                # #get user_id by cbpo_fingerPrintId (user fingerprint id) 
                # fpids=self.pool.get('hr.employee').search(cr,uid,[('cbpo_fingerPrintId'  , '=' , employee_id)],order=None)
                # if(len(fpids)>0):
                    # userid=fpids[0]
                    # if checktype == "I":
                        # action = "sign_in"
                        # aa='in'
                    # else:
                        # action = "sign_out"
                        # aa='out'
                    
                    # self.pool.get('hr.attendance').create(cr,uid,{'employee_id':userid, 'name':name, 'action':action ,'compute':'0', 'mydata':'0' })
                    
                    
# # -------------- get last action in db --------------------
# #              
# #                     
# #           
            # except psycopg2.DatabaseError, e:
                # raise osv.except_osv('Error!', 'database error : ' + e.message)
                # print 'error'
# #             #con.commit()
        # concon = 'momo'
Update()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
