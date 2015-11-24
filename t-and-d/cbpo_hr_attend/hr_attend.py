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
import math
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime,timedelta


class hr_contract2(osv.osv):

    _inherit="hr.contract"
    _columns = {
        'month_discip_in': fields.float('Hours Deduction',readonly=True),
        'month_discip':fields.char('Month Deduction & Overtime' ,readonly=True,size=32),
        'lastupdate':fields.char('Last Update' , readonly=True,size=32),
        'working_hour': fields.float('Working Hours'),
        'days_discip_in': fields.float('Days Discip',   size=32),
        'month_overtime': fields.float('Hours Overtime',readonly=True),




    }
    _defaults = {
        'working_hour': '8'
    }


hr_contract2()

class res_company2(osv.osv):

    _inherit="res.company"
    _columns = {
        'start_day': fields.integer('Start Day Month'),
        'tt_in': fields.integer('Time Zone Diff In'),
        'tt_out': fields.integer('Time Zone Diff Out'),


    }
    _defaults = {
        'start_day': '1',
        'tt_in': '2',
        'tt_out': '2',
		 
    }


hr_contract2()



class hr_attendance(osv.osv):

    _inherit="hr.attendance"


    def _altern_si_so(self, cr, uid, ids, context=None):
        """ Alternance sign_in/sign_out check.
            Previous (if exists) must be of opposite action.
            Next (if exists) must be of opposite action.
        """

        return True
    def _day_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, '')
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = time.strftime('%Y-%m-%d', time.strptime(obj.name, '%Y-%m-%d %H:%M:%S'))
        return res
    def _nameday_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, '')
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = time.strftime('%A', time.strptime(obj.name, '%Y-%m-%d %H:%M:%S'))
        return res
    _columns = {
        'name': fields.datetime('Date', required=True, select=1),
        'action': fields.selection([('sign_in', 'Sign In'), ('sign_out', 'Sign Out'), ('action','Action')], 'Action', required=True),
        'action_desc': fields.many2one("hr.action.reason", "Action Reason", domain="[('action_type', '=', action)]", help='Specifies the reason for Signing In/Signing Out in case of extra hours.'),
        'employee_id': fields.many2one('hr.employee', "Employee", required=True, select=True),
        'day': fields.function(_day_compute, type='char', string='Day', store=True, select=1, size=32),
        'day_name': fields.function(_nameday_compute, type='char', string='Day', store=True, select=1, size=32),
        'compute' : fields.char('compute',   size=32),
        'mydata':fields.char('mydata',   size=32),
    }
    _defaults = {
        'name': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'), #please don't remove the lambda, if you remove it then the current time will not change

        'compute': '0'
    }
    _constraints = [(_altern_si_so, 'Error HASHEM', ['action'])]

class hr_fingerprint_data(osv.osv):
    _name = "hr.fingerprint_data"
    _description = "fingerprint data Attendance .. "


    _columns = {
        'name': fields.datetime('DateTime',   select=1),
        'fid' : fields.integer('Finger ID',  required=True, size=32),
        'action':fields.char('action',   size=32),
        'compute' : fields.char('compute',   size=32),

    }
    _defaults = {
        'compute': '0'
    }



class hr_attendance2(osv.osv):
    _name = "hr.attendance2"
    _description = "Attendance .. "
    
    


    def _day_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, '')
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = time.strftime('%Y-%m-%d', time.strptime(obj.name, '%Y-%m-%d %H:%M:%S'))
        return res


    def _day_int_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, 0)
        for obj in self.browse(cr, uid, ids, context=context):
            y=time.strftime('%Y', time.strptime(obj.name, '%Y-%m-%d %H:%M:%S'))
            m=time.strftime('%m', time.strptime(obj.name, '%Y-%m-%d %H:%M:%S'))
            d=time.strftime('%d', time.strptime(obj.name, '%Y-%m-%d %H:%M:%S'))
            all=y+m+d
            allint=int(all)
            res[obj.id] = allint
        return res

    def _diff_in_compute(self, cr, uid, ids, fieldnames, args, context=None):
        
        _str_from_mints=''
        res = dict.fromkeys(ids, '')
        
        for wizared in self.browse(cr, uid, ids, context=context):
            state_come=''
            _delta_from=''
            
            name=datetime.strptime(wizared.name,'%Y-%m-%d %H:%M:%S')
            numberofdate=name.strftime('%w')



            #-------------

            #0000000000000
            employee_id=int(wizared.employee_id)
            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
            if(len(employee_ids)>0):
                row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours'])
                lenthdata1=len(row_data_contract)
                if(lenthdata1>0):
                    working_hours=row_data_contract[0]['working_hours'][0]
                    calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                    if(len(calendar_ids)>0):
                        row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])          
                        lenthdata2=len(row_data_calendar)
                        if(lenthdata2>0):
                            hour_from =   row_data_calendar[0]['hour_from']
                            hour_to   =  row_data_calendar[0]['hour_to']   
                            
                            t_in = wizared.time_in
                            if( ( wizared.state=='in_out' or  wizared.state=='in' ) and t_in):
                                
                                #hour_from   =  wizared.schedule_time_in
                                intfrom=int(hour_from)
                                intmintfrom=int( hour_from-intfrom )
                                str_time_from=str(intfrom)+':'+str(intmintfrom)+':00'
                                from_sec=intfrom*60*60+intmintfrom*60
                                my_time_in_fff=datetime.strptime(t_in,'%Y-%m-%d %H:%M:%S') 
                                my_time_in=my_time_in_fff.strftime('%H:%M:%S') 
                                my_time_in_h=int(my_time_in_fff.strftime('%H'))+2
                                my_time_in_m=int(my_time_in_fff.strftime('%M'))
                                my_time_in_s=int(my_time_in_fff.strftime('%S'))
                                my_time_in_sec=my_time_in_h*60*60+my_time_in_m*60+my_time_in_s
                                row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, [calendar_ids[0]],['name','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','13','14'])
                                if(len(row_data_discipline)>0):
                                    s=''
                                if(my_time_in_sec<from_sec):
                                    state_come='Early'
                                    diff_come=from_sec-my_time_in_sec
                                elif(my_time_in_sec>from_sec):
                                    state_come='Late'
                                    diff_come=my_time_in_sec-from_sec
                                         
                                else:
                                    state_come='InTime'
                                    diff_come=from_sec-my_time_in_sec

                                time_delta_from_sec=diff_come
                                abs_from_sec=abs(time_delta_from_sec)

                                _from_mints=float(abs_from_sec)/float(60)
                                _str_from_mints=str(_from_mints)
                                _from_h_0=float(abs_from_sec)/float(3600)

                                _from_h=int(math.floor(_from_h_0))

                                _from_m_0=  float( (_from_h_0-_from_h)*60)
                                _from_m=int(math.floor(_from_m_0))
                                _from_s=  int( (_from_m_0-_from_m)*60)  
                                zero_sec=''
                                zero_met='' 
                                if(_from_s<10):
                                    zero_sec='0'
                                    
                                if(_from_m<10):
                                    zero_met='0'   
                                _delta_from=str(_from_h)+':'+zero_met+str(_from_m)+':'+ zero_sec+str(_from_s)
                                        # state_come
                                        # _delta_from
                            res[wizared.id] = state_come+'||'+_delta_from
                            #res[wizared.id] = state_come+'||'+_str_from_mints

        return res
    
    def _schedule_out_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, '')
        for wizared in self.browse(cr, uid, ids, context=context):
            _schedule_time_out=0.00
            
            name=datetime.strptime(wizared.name,'%Y-%m-%d %H:%M:%S') 
            numberofdate=name.strftime('%w')
            
            employee_id=int(wizared.employee_id)
            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
            if(len(employee_ids)>0):
                row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours'])
                lenthdata1=len(row_data_contract)
                if(lenthdata1>0):
                    working_hours=row_data_contract[0]['working_hours'][0]
                    calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                    if(len(calendar_ids)>0):
                        row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])          
                        lenthdata2=len(row_data_calendar)
                        if(lenthdata2>0):
                            _schedule_time_in =   row_data_calendar[0]['hour_from']
                            _schedule_time_out   =  row_data_calendar[0]['hour_to']    
            
        
            res[wizared.id] = _schedule_time_out 
                            
        return res  
    
    def _schedule_in_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, '')
        for wizared in self.browse(cr, uid, ids, context=context):
            _schedule_time_in=0.00
            
            name=datetime.strptime(wizared.name,'%Y-%m-%d %H:%M:%S') 
            numberofdate=name.strftime('%w')
            
            employee_id=int(wizared.employee_id)
            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
            if(len(employee_ids)>0):
                row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours'])
                lenthdata1=len(row_data_contract)
                if(lenthdata1>0):
                    working_hours=row_data_contract[0]['working_hours'][0]
                    calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                    if(len(calendar_ids)>0):
                        row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])          
                        lenthdata2=len(row_data_calendar)
                        if(lenthdata2>0):
                            _schedule_time_in =   row_data_calendar[0]['hour_from']
                            _schedule_time_out   =  row_data_calendar[0]['hour_to']    
            
        
            res[wizared.id] = _schedule_time_in 
                            
        return res  
    
    def _diff_out_compute(self, cr, uid, ids, fieldnames, args, context=None):
        _str_to_mints=''
        res = dict.fromkeys(ids, '')
        for wizared in self.browse(cr, uid, ids, context=context):
            state_leave=''
            _delta_to=''
            
            name=datetime.strptime(wizared.name,'%Y-%m-%d %H:%M:%S') 
            numberofdate=name.strftime('%w')
            
            employee_id=int(wizared.employee_id)
            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
            if(len(employee_ids)>0):
                row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours'])
                lenthdata1=len(row_data_contract)
                if(lenthdata1>0):
                    working_hours=row_data_contract[0]['working_hours'][0]
                    calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                    if(len(calendar_ids)>0):
                        row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])          
                        lenthdata2=len(row_data_calendar)
                        if(lenthdata2>0):
                            hour_from =   row_data_calendar[0]['hour_from']
                            hour_to   =  row_data_calendar[0]['hour_to']    
                            t_out = wizared.time_out
                            if( ( wizared.state=='in_out' or  wizared.state=='out' )  and t_out):
                                
#                                hour_to   =  wizared.schedule_time_out
                                intto=int(hour_to)
                                intmintto=int( hour_to-intto )
                                str_time_to=str(intto)+':'+str(intmintto)+':00'
                                to_sec=intto*60*60+intmintto*60
                                my_time_out_fff=datetime.strptime(t_out,'%Y-%m-%d %H:%M:%S') 
                                my_time_out=my_time_out_fff.strftime('%H:%M:%S') 
                                my_time_out_h=int(my_time_out_fff.strftime('%H'))+2
                                my_time_out_m=int(my_time_out_fff.strftime('%M'))
                                my_time_out_s=int(my_time_out_fff.strftime('%S'))
                                my_time_out_sec=int(my_time_out_h)*60*60+int(my_time_out_m)*60+int(my_time_out_s)
                                    
                                if(my_time_out_sec<to_sec):
                                    state_leave='Early'
                                    diff_leave=int(to_sec)-int(my_time_out_sec)
                                elif(my_time_out_sec>to_sec):
                                    state_leave='Late'
                                    diff_leave=int(my_time_out_sec)-int(to_sec)
                                else:
                                    state_leave='InTime'
                                    diff_leave=to_sec-my_time_out_sec

                                time_delta_to_sec=my_time_out_sec
                                abs_to_sec=abs(time_delta_to_sec)
                                _to_mints=int(abs_to_sec)/int(60)
                                _str_to_mints=str(_to_mints)
                                _to_h_0=float(abs_to_sec)/float(3600)

                                _to_h=int(math.floor(_to_h_0))
                                _to_m_0=  float( (_to_h_0-_to_h)*60)
                                _to_m=int(math.floor(_to_m_0))
                                _to_s=  int( (_to_m_0-_to_m)*60)  
                                zero_sec=''
                                zero_met='' 
                                if(_to_s<10):
                                    zero_sec='0'
                                else:
                                    zero_sec=''
                                        
                                if(_to_m<10):
                                    zero_met='0'
                                else:
                                    zero_met=''
                                _delta_to=str(_to_h)+':'+zero_met+str(_to_m)+':'+ zero_sec+str(_to_s)
                                             
                            res[wizared.id] = state_leave+'||'+_delta_to

                            #res[wizared.id] = state_leave+'||'+_str_to_mints
                            
        return res     
    def _disc_in_compute(self, cr, uid, ids, fieldnames, args, context=None):
        _str_to_mints=''
        res = dict.fromkeys(ids, '')
        for wizared in self.browse(cr, uid, ids, context=context):
            
            #-------------- start ---------------
            
            state_come=''
            _delta_from=''
            
            name=datetime.strptime(wizared.name,'%Y-%m-%d %H:%M:%S') 
            numberofdate=name.strftime('%w')

            employee_id=int(wizared.employee_id)
            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
            if(len(employee_ids)>0):
                row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours'])
                lenthdata1=len(row_data_contract)
                if(lenthdata1>0):
                    working_hours=row_data_contract[0]['working_hours'][0]
                    calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                    if(len(calendar_ids)>0):
                        row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])          
                        lenthdata2=len(row_data_calendar)
                        if(lenthdata2>0):
                            hour_from =   row_data_calendar[0]['hour_from']
                            hour_to   =  row_data_calendar[0]['hour_to']   
                            
                            t_in = wizared.time_in
                            if( ( wizared.state=='in_out' or  wizared.state=='in' ) and t_in):
                                
                                #hour_from   =  wizared.schedule_time_in
                                intfrom=int(hour_from)
                                intmintfrom=int( hour_from-intfrom )
                                str_time_from=str(intfrom)+':'+str(intmintfrom)+':00'
                                from_sec=intfrom*60*60+intmintfrom*60
                                my_time_in_fff=datetime.strptime(t_in,'%Y-%m-%d %H:%M:%S') 
                                my_time_in=my_time_in_fff.strftime('%H:%M:%S') 
                                my_time_in_h=int(my_time_in_fff.strftime('%H'))+2
                                my_time_in_m=int(my_time_in_fff.strftime('%M'))
                                my_time_in_s=int(my_time_in_fff.strftime('%S'))
                                my_time_in_sec=my_time_in_h*60*60+my_time_in_m*60+my_time_in_s
                                
                                if(my_time_in_sec<from_sec):
                                    state_come='Early'
                                    diff_come=from_sec-my_time_in_sec
                                elif(my_time_in_sec>from_sec):
                                    state_come='Late'
                                    diff_come=my_time_in_sec-from_sec
                                         
                                else:
                                    state_come='InTime'
                                    diff_come=from_sec-my_time_in_sec

                                time_delta_from_sec=diff_come
                                abs_from_sec=abs(time_delta_from_sec)

                                _from_mints=float(abs_from_sec)/float(60)
                                _str_from_mints=str(_from_mints)
                                _from_h_0=float(abs_from_sec)/float(3600)

                                _from_h=int(math.floor(_from_h_0))

                                _from_m_0=  float( (_from_h_0-_from_h)*60)
                                _from_m=int(math.floor(_from_m_0))
                                _from_s=  int( (_from_m_0-_from_m)*60)  
                                zero_sec=''
                                zero_met='' 
                                if(_from_s<10):
                                    zero_sec='0'
                                    
                                if(_from_m<10):
                                    zero_met='0'   
                                _delta_from=str(_from_h)+':'+zero_met+str(_from_m)+':'+ zero_sec+str(_from_s)
                                        # state_come
                                        # _delta_from
                            #res[wizared.id] = state_come+'||'+_delta_from
                            
            # ---------------- end -----------------
            #aaaa=wizared.diff_time_in
            n=''
            desss='0'
            alltime=0
            if(_delta_from!=''):
                arr_time=_delta_from.split(':')
                h=int(arr_time[0])*60
                m=int(arr_time[1])
                alltime=int(h+m)
            if(state_come=='Late'):
                n='met25ar '+str(alltime)
                discipline_ids=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours),('daytype','=','late_in')  ] ,order='t_from')
                if(len(discipline_ids)>0):
                    
                    for discipline_id in discipline_ids:
                        row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id,['name','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','l3','l4'])
                        t_from=row_data_discipline['t_from']
                        t_to=row_data_discipline['t_to']
                        dname=row_data_discipline['name']
                        if( t_from<alltime and t_to>=alltime ):
                            mydiscipline_ids=self.pool.get('hr.attendance2').search(cr,uid,[('discip_in_id' , '=' , dname),('employee_id' , '=' , employee_id) ] ,order='name')
                            counnt=len(mydiscipline_ids)+1
                            s=counnt
                            if(s==0 and desss=='0'):
                                desss=row_data_discipline['d1']
                                if(row_data_discipline['l1']!=0):
                                    desss=str(row_data_discipline['l1'])+'Day'
                            elif(s==1 and desss=='0'):
                                desss=row_data_discipline['d2']
                                if(row_data_discipline['l2']!=0):
                                    desss=str(row_data_discipline['l2'])+'Day'
                            elif(s==2 and desss=='0'):
                                desss=row_data_discipline['d3']
                                if(row_data_discipline['l3']!=0):
                                    desss=str(row_data_discipline['l3'])+'Day'
                            elif(s>2 and desss=='0'):
                                desss=row_data_discipline['d4']
                                if(row_data_discipline['l4']!=0):
                                    desss=str(row_data_discipline['l4'])+'Day'
                            desss=str(desss)
                     
                
            
            res[wizared.id] =desss
        return res  

    
    def _disc_in_id_count_compute(self, cr, uid, ids, fieldnames, args, context=None):
        _str_to_mints=''
        res = dict.fromkeys(ids, '')
        for wizared in self.browse(cr, uid, ids, context=context):
            
            #-------------- start ---------------
            
            state_come=''
            _delta_from=''
            
            name=datetime.strptime(wizared.name,'%Y-%m-%d %H:%M:%S') 
            numberofdate=name.strftime('%w')

            employee_id=int(wizared.employee_id)
            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
            if(len(employee_ids)>0):
                row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours'])
                lenthdata1=len(row_data_contract)
                if(lenthdata1>0):
                    working_hours=row_data_contract[0]['working_hours'][0]
                    calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                    if(len(calendar_ids)>0):
                        row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])          
                        lenthdata2=len(row_data_calendar)
                        if(lenthdata2>0):
                            hour_from =   row_data_calendar[0]['hour_from']
                            hour_to   =  row_data_calendar[0]['hour_to']   
                            
                            t_in = wizared.time_in
                            if( ( wizared.state=='in_out' or  wizared.state=='in' ) and t_in):
                                
                                #hour_from   =  wizared.schedule_time_in
                                intfrom=int(hour_from)
                                intmintfrom=int( hour_from-intfrom )
                                str_time_from=str(intfrom)+':'+str(intmintfrom)+':00'
                                from_sec=intfrom*60*60+intmintfrom*60
                                my_time_in_fff=datetime.strptime(t_in,'%Y-%m-%d %H:%M:%S') 
                                my_time_in=my_time_in_fff.strftime('%H:%M:%S') 
                                my_time_in_h=int(my_time_in_fff.strftime('%H'))+2
                                my_time_in_m=int(my_time_in_fff.strftime('%M'))
                                my_time_in_s=int(my_time_in_fff.strftime('%S'))
                                my_time_in_sec=my_time_in_h*60*60+my_time_in_m*60+my_time_in_s
                                
                                if(my_time_in_sec<from_sec):
                                    state_come='Early'
                                    diff_come=from_sec-my_time_in_sec
                                elif(my_time_in_sec>from_sec):
                                    state_come='Late'
                                    diff_come=my_time_in_sec-from_sec
                                         
                                else:
                                    state_come='InTime'
                                    diff_come=from_sec-my_time_in_sec

                                time_delta_from_sec=diff_come
                                abs_from_sec=abs(time_delta_from_sec)

                                _from_mints=float(abs_from_sec)/float(60)
                                _str_from_mints=str(_from_mints)
                                _from_h_0=float(abs_from_sec)/float(3600)

                                _from_h=int(math.floor(_from_h_0))

                                _from_m_0=  float( (_from_h_0-_from_h)*60)
                                _from_m=int(math.floor(_from_m_0))
                                _from_s=  int( (_from_m_0-_from_m)*60)  
                                zero_sec=''
                                zero_met='' 
                                if(_from_s<10):
                                    zero_sec='0'
                                    
                                if(_from_m<10):
                                    zero_met='0'   
                                _delta_from=str(_from_h)+':'+zero_met+str(_from_m)+':'+ zero_sec+str(_from_s)
                                        # state_come
                                        # _delta_from
                            #res[wizared.id] = state_come+'||'+_delta_from
                            
            # ---------------- end -----------------
            #aaaa=wizared.diff_time_in
            n=''
            counnt=0
            alltime=0
            if(_delta_from!=''):
                arr_time=_delta_from.split(':')
                h=int(arr_time[0])*60
                m=int(arr_time[1])
                alltime=int(h+m)
            if(state_come=='Late'):
                
                discipline_ids=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('daytype','=','late_in') ] ,order='t_from')
                if(len(discipline_ids)>0):
                    
                    for discipline_id in discipline_ids:
                        row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id,['name','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','13','14'])     
                        t_from=row_data_discipline['t_from']
                        t_to=row_data_discipline['t_to']
                        dname=row_data_discipline['name']
                         

                        if( t_from<alltime and t_to>=alltime ):
                             
                            mydiscipline_ids=self.pool.get('hr.attendance2').search(cr,uid,[('discip_in_id' , '=' , dname),('employee_id' , '=' , employee_id) ] ,order='name')
                            counnt=len(mydiscipline_ids)+1
                             
                
            
            res[wizared.id] =counnt
        return res  
    def _disc_in_id_compute(self, cr, uid, ids, fieldnames, args, context=None):
        _str_to_mints=''
        res = dict.fromkeys(ids, '')
        for wizared in self.browse(cr, uid, ids, context=context):
            
            #-------------- start ---------------
            
            state_come=''
            _delta_from=''
            
            name=datetime.strptime(wizared.name,'%Y-%m-%d %H:%M:%S') 
            numberofdate=name.strftime('%w')

            employee_id=int(wizared.employee_id)
            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
            if(len(employee_ids)>0):
                row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours'])
                lenthdata1=len(row_data_contract)
                if(lenthdata1>0):
                    working_hours=row_data_contract[0]['working_hours'][0]
                    calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                    if(len(calendar_ids)>0):
                        row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])          
                        lenthdata2=len(row_data_calendar)
                        if(lenthdata2>0):
                            hour_from =   row_data_calendar[0]['hour_from']
                               
                            
                            t_in = wizared.time_in
                            if( ( wizared.state=='in_out' or  wizared.state=='in' ) and t_in):
                                
                                hour_from   =  wizared.schedule_time_in
                                intfrom=int(hour_from)
                                intmintfrom=int( hour_from-intfrom )
                                 
                                from_sec=intfrom*60*60+intmintfrom*60
                                my_time_in_fff=datetime.strptime(t_in,'%Y-%m-%d %H:%M:%S') 
                                 
                                my_time_in_h=int(my_time_in_fff.strftime('%H'))+2
                                my_time_in_m=int(my_time_in_fff.strftime('%M'))
                                my_time_in_s=int(my_time_in_fff.strftime('%S'))
                                my_time_in_sec=my_time_in_h*60*60+my_time_in_m*60+my_time_in_s
                                
                                if(my_time_in_sec<from_sec):
                                    state_come='Early'
                                    diff_come=from_sec-my_time_in_sec
                                elif(my_time_in_sec>from_sec):
                                    state_come='Late'
                                    diff_come=my_time_in_sec-from_sec
                                         
                                else:
                                    state_come='InTime'
                                    diff_come=from_sec-my_time_in_sec

                                time_delta_from_sec=diff_come
                                abs_from_sec=abs(time_delta_from_sec)

                                _from_mints=float(abs_from_sec)/float(60)
                                _str_from_mints=str(_from_mints)
                                _from_h_0=float(abs_from_sec)/float(3600)

                                _from_h=int(math.floor(_from_h_0))

                                _from_m_0=  float( (_from_h_0-_from_h)*60)
                                _from_m=int(math.floor(_from_m_0))
                                _from_s=  int( (_from_m_0-_from_m)*60)  
                                zero_sec=''
                                zero_met='' 
                                if(_from_s<10):
                                    zero_sec='0'
                                    
                                if(_from_m<10):
                                    zero_met='0'   
                                _delta_from=str(_from_h)+':'+zero_met+str(_from_m)+':'+ zero_sec+str(_from_s)
                                        # state_come
                                        # _delta_from
                            #res[wizared.id] = state_come+'||'+_delta_from
                            
            # ---------------- end -----------------
            #aaaa=wizared.diff_time_in
             
            mydissid=0
            alltime=0
            if(_delta_from!=''):
                arr_time=_delta_from.split(':')
                h=int(arr_time[0])*60
                m=int(arr_time[1])
                alltime=int(h+m)
            if(state_come=='Late'):
                 
                discipline_ids=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('daytype','=','late_in') ] ,order='t_from')
                if(len(discipline_ids)>0):
                    
                    for discipline_id in discipline_ids:
                        row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id,['name','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','13','14'])     
                        t_from=row_data_discipline['t_from']
                        t_to=row_data_discipline['t_to']
                        
                        if( t_from<alltime and t_to>=alltime ):
                             
                                
                            if(mydissid==0):
                                mydissid=row_data_discipline['name']
                            
                             
                     
                
            
            res[wizared.id] =mydissid
            res[wizared.id] =0
        return res
    
    
    def _calendar_compute(self, cr, uid, ids, fieldnames, args, context=None):
        working_hours=0
        res = dict.fromkeys(ids, '')
        for wizared in self.browse(cr, uid, ids, context=context):
             
            
            employee_id=int(wizared.employee_id)
            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
            if(len(employee_ids)>0):
                row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours'])
                lenthdata1=len(row_data_contract)
                if(lenthdata1>0):
                    working_hours=row_data_contract[0]['working_hours'][0]
                    
                     
        
            res[wizared.id] = working_hours 
                            
        return res
    
    def action_compute_field(self, cr, uid, ids, context=None):

        _str_to_mints=''
        res = dict.fromkeys(ids, '')
        for wizared in self.browse(cr, uid, ids, context=context):

            #-------------- start ---------------

            state_come=''
            _delta_from=''

            name=datetime.strptime(wizared.name,'%Y-%m-%d %H:%M:%S')
            numberofdate=name.strftime('%w')

            employee_id=int(wizared.employee_id)
            employee_ids=self.pool.get('hr.contract').search(cr,uid,[('employee_id' , '=' , employee_id)] ,order='id')
            if(len(employee_ids)>0):
                row_data_contract = self.pool.get('hr.contract').read(cr, uid, [employee_ids[0]],['working_hours'])
                lenthdata1=len(row_data_contract)
                if(lenthdata1>0):
                    working_hours=row_data_contract[0]['working_hours'][0]
                    calendar_ids=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('dayofweek' , '=',numberofdate)] , context=context)
                    if(len(calendar_ids)>0):
                        row_data_calendar = self.pool.get('resource.calendar.attendance').read(cr, uid, [calendar_ids[0]],['dayofweek','hour_from','hour_to'])
                        lenthdata2=len(row_data_calendar)
                        if(lenthdata2>0):
                            hour_from =   row_data_calendar[0]['hour_from']
                            hour_to   =  row_data_calendar[0]['hour_to']

                            t_in = wizared.time_in
                            if( ( wizared.state=='in_out' or  wizared.state=='in' ) and t_in):

                                #hour_from   =  wizared.schedule_time_in
                                intfrom=int(hour_from)
                                intmintfrom=int( hour_from-intfrom )
                                str_time_from=str(intfrom)+':'+str(intmintfrom)+':00'
                                from_sec=intfrom*60*60+intmintfrom*60
                                my_time_in_fff=datetime.strptime(t_in,'%Y-%m-%d %H:%M:%S')
                                my_time_in=my_time_in_fff.strftime('%H:%M:%S')
                                my_time_in_h=int(my_time_in_fff.strftime('%H'))+2
                                my_time_in_m=int(my_time_in_fff.strftime('%M'))
                                my_time_in_s=int(my_time_in_fff.strftime('%S'))
                                my_time_in_sec=my_time_in_h*60*60+my_time_in_m*60+my_time_in_s

                                if(my_time_in_sec<from_sec):
                                    state_come='Early'
                                    diff_come=from_sec-my_time_in_sec
                                elif(my_time_in_sec>from_sec):
                                    state_come='Late'
                                    diff_come=my_time_in_sec-from_sec

                                else:
                                    state_come='InTime'
                                    diff_come=from_sec-my_time_in_sec

                                time_delta_from_sec=diff_come
                                abs_from_sec=abs(time_delta_from_sec)

                                _from_mints=float(abs_from_sec)/float(60)
                                _str_from_mints=str(_from_mints)
                                _from_h_0=float(abs_from_sec)/float(3600)

                                _from_h=int(math.floor(_from_h_0))

                                _from_m_0=  float( (_from_h_0-_from_h)*60)
                                _from_m=int(math.floor(_from_m_0))
                                _from_s=  int( (_from_m_0-_from_m)*60)
                                zero_sec=''
                                zero_met=''
                                if(_from_s<10):
                                    zero_sec='0'

                                if(_from_m<10):
                                    zero_met='0'
                                _delta_from=str(_from_h)+':'+zero_met+str(_from_m)+':'+ zero_sec+str(_from_s)
                                        # state_come
                                        # _delta_from
                            #res[wizared.id] = state_come+'||'+_delta_from

            # ---------------- end -----------------
            #aaaa=wizared.diff_time_in


            #-------- count -------------
            n=''
            counnt=0
            alltime=0
            if(_delta_from!=''):
                arr_time=_delta_from.split(':')
                h=int(arr_time[0])*60
                m=int(arr_time[1])
                alltime=int(h+m)
            if(state_come=='Late'):

                discipline_ids=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours) ,('daytype','=','late_in') ] ,order='t_from')
                if(len(discipline_ids)>0):

                    for discipline_id in discipline_ids:
                        row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id,['name','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','13','14'])
                        t_from=row_data_discipline['t_from']
                        t_to=row_data_discipline['t_to']
                        dname=row_data_discipline['name']


                        if( t_from<alltime and t_to>=alltime ):

                            mydiscipline_ids=self.pool.get('hr.attendance2').search(cr,uid,[('discip_in_id' , '=' , dname),('employee_id' , '=' , employee_id) ] ,order='name')
                            counnt=len(mydiscipline_ids)+1



            res[wizared.id] =counnt

            # --------- end count ---------------------
            # --------- Start discipline ID ---------------------

            mydissid=0
            alltime=0
            if(_delta_from!=''):
                arr_time=_delta_from.split(':')
                h=int(arr_time[0])*60
                m=int(arr_time[1])
                alltime=int(h+m)
            if(state_come=='Late'):

                discipline_ids=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours),('daytype','=','late_in')  ] ,order='t_from')
                if(len(discipline_ids)>0):

                    for discipline_id in discipline_ids:
                        row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id,['name','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','13','14'])
                        t_from=row_data_discipline['t_from']
                        t_to=row_data_discipline['t_to']

                        if( t_from<alltime and t_to>=alltime ):


                            if(mydissid==0):
                                mydissid=row_data_discipline['name']





            res[wizared.id] =mydissid


            # --------- End discipline ID ---------------------
            # --------- Start discipline Value ---------------------

            n=''
            desss='0'
            alltime=0
            if(_delta_from!=''):
                arr_time=_delta_from.split(':')
                h=int(arr_time[0])*60
                m=int(arr_time[1])
                alltime=int(h+m)
            if(state_come=='Late'):
                n='met25ar '+str(alltime)
                discipline_ids=self.pool.get('hr.discipline').search(cr,uid,[('calendar_id' , '=' , working_hours),('daytype','=','late_in') ] ,order='t_from')
                if(len(discipline_ids)>0):

                    for discipline_id in discipline_ids:
                        row_data_discipline = self.pool.get('hr.discipline').read(cr, uid, discipline_id,['name','daytype', 't_from','t_to','d1','d2','d3','d4','l1','l2','l3','l4'])
                        t_from=row_data_discipline['t_from']
                        t_to=row_data_discipline['t_to']
                        dname=row_data_discipline['name']
                        if( t_from<alltime and t_to>=alltime ):
                            mydiscipline_ids=self.pool.get('hr.attendance2').search(cr,uid,[('discip_in_id' , '=' , dname),('employee_id' , '=' , employee_id) ] ,order='name')
                            counnt=len(mydiscipline_ids)+1
                            s=counnt
                            if(s==0 and desss=='0'):
                                desss=row_data_discipline['d1']
                                if(row_data_discipline['l1']!=0):
                                    desss=str(row_data_discipline['l1'])+'Day'
                            elif(s==1 and desss=='0'):
                                desss=row_data_discipline['d2']
                                if(row_data_discipline['l2']!=0):
                                    desss=str(row_data_discipline['l2'])+'Day'
                            elif(s==2 and desss=='0'):
                                desss=row_data_discipline['d3']
                                if(row_data_discipline['l3']!=0):
                                    desss=str(row_data_discipline['l3'])+'Day'
                            elif(s>2 and desss=='0'):
                                desss=row_data_discipline['d4']
                                if(row_data_discipline['l4']!=0):
                                    desss=str(row_data_discipline['l4'])+'Day'
                            desss=str(desss)



            res[wizared.id] =desss


            # --------- End discipline Value ---------------------

            counnt
            mydissid
            desss
            self.write(cr, uid, wizared.id, {'compute': '1' , 'discip_in_id': mydissid,'discip_in_id_count': counnt ,'discip_in': desss})



    _columns = {
        
        'name': fields.datetime('Date'),
        'action': fields.selection([('sign_in', 'Sign In'), ('sign_out', 'Sign Out'), ('sign_in_out', 'IN & OUT'), ('action','Action')], 'Action', required=True),
        'action_desc': fields.many2one("hr.action.reason", "Action Reason", domain="[('action_type', '=', action)]", help='Specifies the reason for Signing In/Signing Out in case of extra hours.'),
        'employee_id': fields.many2one('hr.employee', "Employee", required=True, select=True),
        'day': fields.function(_day_compute, type='char', string='Day', store=True, select=1, size=32),
        'dayint': fields.function(_day_int_compute, type='integer', string='Day', store=True, select=1, size=32),
        'schedule_time_in': fields.function(_schedule_in_compute,type='float',string='Schedule IN ',store=True, help='Schedule IN .'),
        'schedule_time_out': fields.function(_schedule_out_compute,type='float',string='Schedule OUT ',store=True, help='Schedule OUT .'),
        'time_in':  fields.datetime('Time IN',  help='Time IN.'),
        'time_out': fields.datetime('Time OUT',  help='Time OUT.'),
        'state': fields.selection([('in', 'In'), ('out', 'Out'), ('in_out','In & Out') ], 'State', required=True),
        # 'diff_time_in': fields.function(_diff_in_compute,type='char',string='Diff IN ',store=True  ,help='Time Difference IN .'),
        # 'diff_time_out': fields.function(_diff_out_compute,type='char',string='Diff OUT ',store=True, help='Time Difference OUT .'),
        'calendar_id':fields.function(_calendar_compute,type='integer',string='calendar',store=True, help='calendar'),
        #
        # 'discip_in': fields.function(_disc_in_compute,type='char',string='Discipline In',store=True,    help='Discipline In.'),
        # 'discip_in_id': fields.function(_disc_in_id_compute,type='integer',string='Discipline ID',store=True,    help='Discipline ID.'),
        #
        # 'discip_in_id_count': fields.function(_disc_in_id_count_compute,type='integer',string='Discipline Count',store=True,    help='Discipline Count.'),

        'diff_time_in': fields.char('Diff IN',    help='Time Difference IN.'),
        'diff_time_out': fields.char('Diff Out',    help='Time Difference Out.'),

        #========================
        'discip_in': fields.char('Discipline In',    help='Discipline In.'),
        'discip_in_id': fields.integer('Discipline In ID',   help='Discipline In ID.'),
        'discip_in_id_count': fields.integer('Discipline In Count',   help='Discipline In Count.'),

        'discip_out': fields.char('Discipline Out',    help='Discipline Out.'),
        'discip_out_id': fields.integer('Discipline Out ID',   help='Discipline Out ID.'),
        'discip_out_id_count': fields.integer('Discipline Out Count',   help='Discipline Out Count.'),

        #========================
        'overtime_in': fields.char('Overtime In',    help='Overtime In.'),
        'overtime_in_id': fields.integer('Overtime In ID',   help='Overtime In ID.'),
        'overtime_in_id_count': fields.integer('Overtime In Count',   help='Overtime In Count.'),

        'overtime_out': fields.char('Overtime Out',    help='Overtime Out.'),
        'overtime_out_id': fields.integer('Overtime Out ID',   help='Overtime Out ID.'),
        'overtime_out_id_count': fields.integer('Overtime Out Count',   help='Overtime Out Count.'),

        #========================


#         'discip_in': fields.char('Discipline In' , size=32),
        'compute':fields.char('compute' , size=32),
        
    }
    _defaults = {
        'name': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'), #please don't remove the lambda, if you remove it then the current time will not change
        'state': 'in',
        'action': 'sign_in_out',
        'compute': '0',

    }

    _order = 'day desc , employee_id asc'

hr_attendance2()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
class hr_attendance3(osv.osv):
    _name = "hr.attendance3"
    _description = "Attendance .. "

    _columns = {
        'employee_id': fields.many2one('hr.employee', "Employee", required=True, select=True),
        'month': fields.char('Month',   size=32),
        'total_discip_in': fields.float('Total Deduction',   size=32),
        'total_overtime': fields.float('Total Overtime',   size=32),
        'days_discip_in': fields.float('Days Deduction',   size=32),
        'lastupdate':fields.char('Last Update' , readonly=True,size=32),
    }
    _order = 'month desc , employee_id asc'

hr_attendance3()
