
import time
import math
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime,timedelta

class calendar2(osv.osv):
    _inherit="calendar.event"


    def create(self, cr, uid, vals, context = None):
        allday = vals.get('allday')
        partner_ids0 = vals.get('partner_ids')
        daytype = vals.get('daytype')
        description = vals.get('description')
        name = vals.get('name')
        start_datetime = vals.get('start_datetime')
        start_date = vals.get('start_date')
        stop_datetime = vals.get('stop_datetime')
        start_date = vals.get('stop_date')
        ppp=0
        ppp2=0
        if(partner_ids0 and len(partner_ids0)>0):
            ppp=len(partner_ids0[0])
            if(ppp>2):
                ppp2=len(partner_ids0[0][2])
                partner_ids=partner_ids0[0][2]

        if(ppp2>0):
            for partner_id in partner_ids:



                employee_ids  = self.pool.get('hr.employee').search(cr,uid,[('address_home_id' , '=' , partner_id)] )
                if(len(employee_ids)>0):
                    employee_id=employee_ids[0]
                    if(allday):

                        daytype='full_day'


                        self.pool.get('hr.excuse').create(cr,uid,{'name':name,'employee_id':employee_id,'daytype':daytype, 'day':start_date,'type':'Mission' , 'state':'Draft' ,'note':description ,   })
                    else:
                        daytype = vals.get('daytype')
                        if(start_datetime and start_datetime.find(':')!=-1):
                            time_in_arr0=start_datetime.split(' ');
                            time_in_arr=time_in_arr0[1].split(':');
                            time_h_in=time_in_arr[0]
                            time_m_in=time_in_arr[1]

                        my_time_in=(int(time_h_in))*60 +int(time_m_in)

                        if(stop_datetime and stop_datetime.find(':')!=-1):
                            time_out_arr0=stop_datetime.split(' ');
                            time_out_arr=time_out_arr0[1].split(':');
                            time_h_out=time_out_arr[0]
                            time_m_out=time_out_arr[1]

                        my_time_out=(int(time_h_out))*60 +int(time_m_out)
                        diff=my_time_out-my_time_in

                        diff_int=diff/60
                        diff_ba2y= diff - (diff_int*60)
                        del_mint=''
                        if(diff_ba2y<10):
                            del_mint='0'

                        del_hour=''
                        if(diff_int<10):
                            del_hour='0'

                        diff_str=del_hour+str(diff_int)+':'+del_mint+str(diff_ba2y)
                        self.pool.get('hr.excuse').create(cr,uid,{'name':name,'employee_id':employee_id,'daytype':daytype,'timeexcuse': diff_str, 'day':start_date,'type':'Mission' , 'state':'Draft' ,'note':description ,   })

                        a='no'

        return super(calendar2, self).create(cr, uid, vals, context=context)


    _columns = {
        'daytype': fields.selection([('late_in', 'Late In'),  ('early_out', 'Early Out')], 'Day Type'),


        }

calendar2()