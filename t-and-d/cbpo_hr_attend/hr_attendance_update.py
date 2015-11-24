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
class Update(models.Model):
    _name = 'hr.attendance.update'
    _columns = {
            'db': fields.selection([('MDBTools','MDBTools'),('Microsoft Access Driver (*.mdb)', 'MS Access Win32'),('Microsoft Access Driver (*.mdb, *.accdb)', 'MS Access Win64'), ('oracle', 'Oracle'),('mysql','MySQL'),('postgres','Postgres')], "DataBase Type"),
            'path':fields.char('Access Path',size=200),
            'dbname':fields.char('DataBase Name',size=200),
            'username':fields.char('User Name',size=15),
            'password':fields.char('password',size=200,password="True"),
            'useingconf': fields.boolean('Useing Data Wizard'),

            'month':fields.integer('Month' ,required=True),
            'year':fields.integer('Year',required=True),


    }


    _defaults = {


    'month':lambda *a: time.strftime('%m'),
    'year':lambda *a: time.strftime('%Y'),
    'path': 'c://attend/att2000.mdb',
    'dbname': 'Checkinout',
    'useingconf':'False'
    }
    def attend_set_data(self,cr,uid,ids=None,context=None):
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
                        name2=name+'-02:00'

                        # raise osv.except_osv('Date Show!', 'name : ' + name+'\n name2 : '+name2)
                        # mydate_name = datetime.strptime(name, fmt)
                        # mydate=mydate_name -  timedelta(hours=-2)
                        # myfinaldate=mydate.strftime("%Y-%m-%d %H:%M:%S")

                        myfinaldate=name
                        actiontype =  str( row_data_fingerprint['action'])

                        fpids=self.pool.get('hr.employee').search(cr,uid,[('cbpo_fingerPrintId'  , '=' , fid)],order=None)
                        if(len(fpids)>0):
                            userid=fpids[0]
                            if actiontype == "I":
                                action = "sign_in"

                            else:
                                action = "sign_out"


                            self.pool.get('hr.attendance').create(cr,uid,{'employee_id':userid, 'name':myfinaldate, 'action':action ,'compute':'0'})
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


        company_data=self.pool.get('res.company').read(cr, uid, cmmppny, ["start_day","tt_in","tt_out"])
        mystartday=int(company_data['start_day'])
        tt_in=int(company_data['tt_in'])
        tt_out=int(company_data['tt_out'])

        y=int(wizared.year)
        m=int(wizared.month)
        m1=0
        y1=0


        if(mystartday>1):
            mystartdayend=mystartday-1
            myendday0=str(mystartdayend)
            mystartday0=str(company_data['start_day'])
            y=int(wizared.year)
            m=int(wizared.month)

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


        # raise osv.except_osv('company ',  '\n s1:'+s1+'\n s2:'+s2)

        conn_ids=self.pool.get('hr.contract').search(cr,uid,[('month_discip' , '!=' , s4)  ] ,order='employee_id')
        self.pool.get('hr.contract').write(cr, uid, conn_ids, {'month_overtime':'0.00','month_discip_in': '0.00','days_discip_in':'0.00','lastupdate':s3 ,'month_discip':s4 }, context)

        # att3_ids=self.pool.get('hr.attendance3').search(cr,uid,[('month' , '=' , s4) ] ,order='month')
        # self.pool.get('hr.attendance3').write(cr, uid, conn_ids, {'total_discip_in': '0.00','lastupdate':s3 ,'month':s4 }, context)



        myList=  []
        ds1=datetime.strptime(s1,"%Y-%m-%d")
        ds2=datetime.strptime(s2,"%Y-%m-%d")
        attend2_ids=self.pool.get('hr.attendance2').search(cr,uid,[('dayint' , '>=' , day_s1),('dayint' , '<=' , day_s2)  ],order='employee_id asc' )

        nn=len(attend2_ids)
        aaa=str(len(attend2_ids))
        # raise osv.except_osv('attendance2 ',  '\n Total:'+aaa+'\n s1:'+s1+'\n s2:'+s2
        # +'\n Ds1:'+str(ds1)+'\n Ds2:'+str(ds2)
        # +'\n day_s1_s:'+str(day_s1)+'\n day_s2_s:'+str(day_s2))
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
        if(nn>0):

            for attendID in attend2_ids:

                disc0=0
                disc1=0
                over0=0
                row_data_attend2 = self.pool.get('hr.attendance2').read(cr, uid, [attendID],['discip_in','overtime_out','discip_out','employee_id','day'])
                if(row_data_attend2[0]['discip_in'] or row_data_attend2[0]['discip_out']):
                    disc00=str(row_data_attend2[0]['discip_in'])
                    disc000=str(row_data_attend2[0]['discip_out'])
                    if(row_data_attend2[0]['discip_in']):
                        if(disc00.find('Day')==-1):
                            disc0_in=float(row_data_attend2[0]['discip_in'])
                            day=False
                            disc_days_in=0
                        else:
                            day=True
                            dayaaaa=disc00.split('Day');
                            disc_days_in=float(dayaaaa[0])
                            # compute day from leaves here
                            disc0_in=0
                    else:
                        disc0=0
                        disc_days_in=0

                    if(row_data_attend2[0]['discip_out']):
                        if(disc000.find('Day')==-1):
                            disc1_out=float(row_data_attend2[0]['discip_out'])
                            day=False
                            disc_days_out=0
                        else:
                            day=True
                            dayaaaa2=disc000.split('Day');
                            disc_days_out=float(dayaaaa2[0])
                            # compute day from leaves here
                            disc1_out=0

                    else:
                        disc1_out=0
                        disc_days_out=0





                if(row_data_attend2[0]['overtime_out']):
                    over0=float(row_data_attend2[0]['overtime_out'])
                else:
                    over0=0



                myid0=str(row_data_attend2[0]['employee_id'][0])

                disc=disc0_in+disc1_out
                disc_days=disc_days_in+disc_days_out
                myid=int(row_data_attend2[0]['employee_id'][0])
                last_over=over0
                last_dis_day=disc_days
                last_dis=disc
                last_id=myid

                if(mylastid!=0):
                    if(mylastid==myid):

                        mysum=mysum+disc
                        mysum_over=mysum_over+float(over0)
                        mysum_disc_days=mysum_disc_days+disc_days
                    else:

                        contract_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',mylastid) ] ,order='employee_id')

                        if(len(contract_ids)>0):

                            mycomp=-1;
                            row_data_contract = self.pool.get('hr.contract').read(cr, uid, contract_ids[0],['working_hour'])
                            working_hour =  float( row_data_contract['working_hour'])
                            mycomp0=float(mysum)/float(100)
                            mycomp1=float(working_hour)
                            # mycomp= mycomp0  * working_hour
                            mycomp= float(mysum)
                            myover=float(mysum_over)

                            self.pool.get('hr.contract').write(cr, uid, contract_ids[0], {'month_overtime': mysum_over ,'month_discip_in': mysum ,'days_discip_in':mysum_disc_days,'lastupdate':s3 ,'month_discip':s4 }, context)

                            attend3_ids=self.pool.get('hr.attendance3').search(cr,uid,[('month' , '=' , s4),('employee_id' , '=' , mylastid) ] ,order='month')
                            at3len=len(attend3_ids)
                            # raise osv.except_osv('Show ',  '\n total:'+str(at3len)+'\n employee_id:'+str(mylastid))
                            if(at3len>0):
                                self.pool.get('hr.attendance3').write(cr, uid, attend3_ids, {'total_overtime': mysum_over ,'total_discip_in': mysum,'days_discip_in':mysum_disc_days, 'lastupdate':s3 ,'month':s4 }, context)
                            else:
                                self.pool.get('hr.attendance3').create(cr,uid,{'total_overtime': mysum_over ,'employee_id':mylastid, 'total_discip_in':mysum ,'days_discip_in':mysum_disc_days, 'month':s4  ,'lastupdate':s3   })

                            mylastid=myid
                            mysum=0
                            mysum_over=0
                            mysum_disc_days=0

                        #raise osv.except_osv('OOO ',  '\n '+str(contract_ids[0])+'\n'+str(last_total_disc))
                        #raise osv.except_osv('Msg nooooooot ',  '\n last_total_disc \n '+str(last_total_disc)+'\n ID='+myid0+'\n mylastID='+str(mylastid))


                else:
                    mylastid=myid
                    mysum=mysum+disc
                    mysum_over=mysum_over+float(over0)
                    mysum_disc_days=mysum_disc_days+disc_days


        end=''
        #
        # last_over
        #         last_dis_day
        #         last_dis
        #         last_id
        contract_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',last_id) ] ,order='employee_id')

        if(len(contract_ids)>0):
            self.pool.get('hr.contract').write(cr, uid, contract_ids[0], {'month_overtime': last_over ,'month_discip_in': last_dis ,'days_discip_in':last_dis_day,'lastupdate':s3 ,'month_discip':s4 }, context)

        attend3_ids=self.pool.get('hr.attendance3').search(cr,uid,[('month' , '=' , s4),('employee_id' , '=' , last_id) ] ,order='month')
        at3len=len(attend3_ids)
        # raise osv.except_osv('Show ',  '\n total:'+str(at3len)+'\n employee_id:'+str(mylastid))
        if(at3len>0):
            self.pool.get('hr.attendance3').write(cr, uid, attend3_ids, {'total_overtime': last_over ,'total_discip_in': last_dis,'days_discip_in':last_dis_day, 'lastupdate':s3 ,'month':s4 }, context)
        else:
            self.pool.get('hr.attendance3').create(cr,uid,{'total_overtime': last_over ,'employee_id':last_id, 'total_discip_in':last_dis ,'days_discip_in':last_dis_day, 'month':s4  ,'lastupdate':s3   })


            # contract_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',mylastid) ] ,order='employee_id')
            # self.pool.get('hr.contract').write(cr, uid, contract_ids[0], {'month_discip_in': mysum ,'lastupdate':s3 }, context)

            #raise osv.except_osv('Msg nooooooot ',  '\n Msg \n '+str(total_disc)+'\n ID='+myid0)


        #raise osv.except_osv('ALL DATA',  '\n Start : '+s1+'\n End : '+s2+'\n Date : '+s3+'\n ALl Employee : '+aaa)


    def update_attend_compute(self,cr,uid,ids=None,context=None):
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


        company_data=self.pool.get('res.company').read(cr, uid, cmmppny, ["start_day","tt_in","tt_out"])
        mystartday=int(company_data['start_day'])
        tt_in=int(company_data['tt_in'])
        tt_out=int(company_data['tt_out'])
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
            mystartdayend=mystartday-1
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


        attend2_ids=self.pool.get('hr.attendance2').search(cr,uid,[('dayint' , '>=' , day_s1),('dayint' , '<=' , day_s2) ],order='time_in asc')
        nn=len(attend2_ids)
        aaa=str(len(attend2_ids))
        # raise osv.except_osv('attendance2 ',  '\n Total:'+aaa+'\n s1:'+s1+'\n s2:'+s2
        # +'\n Ds1:'+str(ds1)+'\n Ds2:'+str(ds2)
        # +'\n day_s1_s:'+str(day_s1)+'\n day_s2_s:'+str(day_s2))

        arr_count=range(0,10000)
        for x in arr_count:
            arr_count[x]=0

        arr_count2=range(0,10000)
        for x2 in arr_count2:
            arr_count2[x2]=0

        arr_count3=range(0,10000)
        for x3 in arr_count3:
            arr_count3[x3]=0

        arr_count4=range(0,10000)
        for x4 in arr_count4:
            arr_count4[x4]=0

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



                time_in=row_data_attend2[0]['time_in']
                time_in_aaaa=row_data_attend2[0]['time_in']

                if(time_in):
                    time_in_date=datetime.strptime(time_in,'%Y-%m-%d %H:%M:%S')
                    numberofdate=time_in_date.strftime('%w')


                    # nameaa.weekday()

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
                     # --------------- end get working hours -------------
                    day=str(row_data_attend2[0]['day'])

                    schedule_time_in=float(hour_from)
                    schedule_time_in_0=int(schedule_time_in)
                    schedule_time_in_1=int((float(schedule_time_in_0)-float(schedule_time_in))*60)
                    s_time_in=schedule_time_in_0*60+schedule_time_in_1
                    my_time=0

                    if(time_in.find(':')!=-1):
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



                        print('employee_id:'+str(employee_id)+' _ discip_in:'+desss+' _ discip_in_id_count:'+str(count_dis_id)+' _ discip_in_id:'+str(mydissid))
                        self.pool.get('hr.attendance2').write(cr, uid, [attendID], {'compute': '1' ,'discip_in':desss,'discip_in_id_count':count_dis_id,'discip_in_id':mydissid ,'diff_time_in':diff_in_str }, context)
                        a_in='' # Late in

                    elif(diff_in==0):
                        #  come in time


                        b=''
                    else:
                        #  early in
                        c=''




                # end  in


                # start   out
                time_out=row_data_attend2[0]['time_out']

                if(time_out):
                    time_out_date=datetime.strptime(time_out,'%Y-%m-%d %H:%M:%S')
                    numberofdate=time_out_date.strftime('%w')


                    # nameaa.weekday()
                    hour_from=0
                    hour_to=0
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
                     # --------------- end get working hours -------------
                    day=str(row_data_attend2[0]['day'])

                    schedule_time_out=float(hour_to)
                    schedule_time_out_0=int(schedule_time_out)
                    schedule_time_out_1=int((float(schedule_time_out_0)-float(schedule_time_out))*60)
                    s_time_out=schedule_time_out_0*60+schedule_time_out_1
                    my_time=0

                    if(time_out.find(':')!=-1):
                        time_out_arr0=time_out.split(' ');
                        time_out_arr=time_out_arr0[1].split(':');
                        time_h=time_out_arr[0]
                        time_m=time_out_arr[1]

                        my_time_out=(int(time_h)+tt_out)*60 +int(time_m)
                        diff_out=my_time_out-s_time_out
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



                        print('employee_id:'+str(employee_id)+' _ discip_out:'+desss2+' _ discip_out_id_count:'+str(count_dis_id2)+' _ discip_out_id:'+str(mydissid2))
                        self.pool.get('hr.attendance2').write(cr, uid, [attendID], {'compute': '1' ,'overtime_out':'0','discip_out':desss2,'discip_out_id_count':count_dis_id2,'discip_out_id':mydissid2,'diff_time_out':diff_out_str2 }, context)
                        a_out='' # Early Out

                    elif(diff_out==0):
                        #  out in time

                        self.pool.get('hr.attendance2').write(cr, uid, [attendID], {'compute': '1' ,'overtime_out':'0','overtime_out_id_count':'0','overtime_out_id':'0','diff_time_out':'In Time' }, context)



                        b=''
                    else:
                         # Late Out
                        diff_out=  abs(diff_out)
                        desss3='0'
                        mydissid3=0
                        count_dis_id3=0
                        dis_id3=0
                        diff_out_str3=''
                        working_hours=0
                        employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')

                        if(len(employee_ids)>0):
                            row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours','working_hour'])
                            lenthdata1=len(row_data_contract)
                        if(lenthdata1>0):
                            working_hours=row_data_contract[0]['working_hours'][0]
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
                                    desss3='0'




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



                                    if(count_dis_id3==1 and desss3=='0'):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss3=float(row_data_discipline['d1'])
                                        else:

                                            desss3=(float(row_data_discipline['d1'])*float(day_hours))/float(100)
                                        if(l1!=0):
                                            desss3=str(l1)+'Day'
                                    elif(count_dis_id3==2 and desss3=='0'):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss3=float(row_data_discipline['d2'])
                                        else:

                                            desss3=(float(row_data_discipline['d2'])*float(day_hours))/float(100)
                                        if(l2!=0):
                                            desss3=str(l2)+'Day'
                                    elif(count_dis_id3==3 and desss3=='0'):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss3=float(row_data_discipline['d3'])
                                        else:
                                            desss3=(float(row_data_discipline['d3'])*float(day_hours))/float(100)
                                        if(l3!=0):
                                            desss3=str(l3)+'Day'
                                    elif(count_dis_id3>3 and desss3=='0'):
                                        if(row_data_discipline['deductype']=='Hours'):

                                            desss3=float(row_data_discipline['d4'])
                                        else:
                                            desss3=(float(row_data_discipline['d4'])*float(day_hours))/float(100)
                                        if(l4!=0):
                                            desss3=str(l4)+'Day'
                                    desss3=str(desss3)



                        print('employee_id:'+str(employee_id)+' _ overtime_out:'+desss3+' _ overtime_out_id_count:'+str(count_dis_id3 )+' _ overtime_out_id:'+str(mydissid3))
                        self.pool.get('hr.attendance2').write(cr, uid, [attendID], {'compute': '1' ,'overtime_out':desss3,'overtime_out_id_count':count_dis_id3,'overtime_out_id':mydissid3,'diff_time_out':diff_out_str3 }, context)

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
                    if(time_out.find(':')!=-1):
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
                    if(time_in.find(':')!=-1):
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
