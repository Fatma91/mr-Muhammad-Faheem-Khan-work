import time

from openerp import fields,osv, models
from openerp.osv import fields, osv



class hr_finger_conf(osv.osv):
    _name = 'hr.finger.conf'
    _columns = {
            'db': fields.selection([('MDBTools','MDBTools'),('Microsoft Access Driver (*.mdb, *.accdb)', 'MS Access Win64'), ('Microsoft Access Driver (*.mdb)', 'MS Access Win32'),('oracle', 'Oracle'),('mysql','MySQL'),('postgres','Postgres')], "DataBase Type"),
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
