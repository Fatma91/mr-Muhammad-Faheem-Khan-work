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

from openerp import tools
from datetime import datetime
from openerp.osv import fields, osv

def _get_due_date(self,cr,uid,ids,field,arg,context=None):
    dued = {}
    for lg in self.browse(cr, uid, ids):
        dued[lg.id] = (datetime.strptime(lg.cbpo_lg_end_date,"%Y-%m-%d")-datetime.now()).days
        ids1 = self.pool.get('cbpo.lg.renew').search(cr, uid, [('cbpo_lg_renew_id', '=', lg.id)])
        for renew in self.pool.get('cbpo.lg.renew').browse(cr, uid, ids1):
            dued[lg.id] = (datetime.strptime(renew.cbpo_lg_renew_end_date,"%Y-%m-%d")-datetime.now()).days
    return dued	
class cbpo_lg(osv.osv):

    def _sel_bank_acc_number_func(self, cr, uid, context=None):
        obj = self.pool.get('res.partner.bank')
        ids = obj.search(cr, uid, [])
        res = obj.read(cr, uid, ids, ['acc_number', 'id'], context)
        res = [(r['id'], r['acc_number']) for r in res]
        return res
			

		
    def onchange_calc_cover_amount(self,cr,uid,ids,cbpo_lg_amount,cbpo_lg_payed_amount,context=None):
        cover_amount = cbpo_lg_amount-cbpo_lg_payed_amount
        val = {
            'cbpo_lg_cover_amount':cover_amount
        }
        return {'value': val}

		
    _name = "cbpo.lg"
    _description = "cbpo LG Mangment"
    _columns = {
        'cbpo_lg_tender': fields.many2one('cbpo.tender','Tender'),
        'cbpo_lg_type': fields.selection((('initial','Initial'), ('final','Final'), ('prepay','Prepay'), ('warrnty','Warrnty'), ('gov','Gov')),'Type letter' ,required=True),
        'cbpo_lg_internal_series': fields.char('Internal Series', size=128),
        'cbpo_lg_bank_series' : fields.char('Bank Series', size=128,required=True),
        'cbpo_lg_direction' : fields.selection((('in','In'), ('out','Out')),'Direction' ,required=True),
        'cbpo_lg_partner': fields.many2one('res.partner', 'Issued from / to',required=True),
        'cbpo_lg_for': fields.char('For', size=128),
        'cbpo_lg_amount': fields.integer('Amount',required=True),
        'cbpo_lg_payed_amount': fields.integer('Payed Amount'),
        'cbpo_lg_description' : fields.text('Description'),
        'cbpo_lg_renewable' : fields.boolean('Renewable'),
        'cbpo_lg_active' : fields.boolean('Active'),
        'cbpo_lg_status': fields.selection((('open','Open'), ('closed','Closed'), ('expired','Expired'), ('collected','Collected')),'Case' ),
        'cbpo_lg_bank_name': fields.many2one('res.bank','Bank Name'),
        'acc_number': fields.many2one('res.partner.bank','Account number'),
        'cbpo_lg_cover_amount' : fields.integer('Cover Amount'),
        'cbpo_lg_per' : fields.integer('Per-payed Amount'),
        'cbpo_lg_bank_fees' : fields.integer('Bank Fees'),
        'cbpo_lg_renew': fields.one2many('cbpo.lg.renew', 'cbpo_lg_renew_id', 'Renew'),
        'cbpo_lg_installment': fields.one2many('cbpo.lg.installment', 'cbpo_lg_installment_id', 'Installment'),
        'cbpo_lg_start_date': fields.date('Start Date',required=True),
        'cbpo_lg_end_date': fields.date('End Date',required=True),
        'cbpo_lg_duration': fields.selection((('1','One Month'), ('3','Three Months'), ('6','Six Months'), ('9','Nine Months'), ('12','Year')),'Period',required=True),
        'cbpo_lg_currency': fields.many2one('res.currency','Currency'),
		'cbpo_lg_due_date' : fields.function(_get_due_date , string="Due Date" , type='integer'),
    }
        
    _defaults = {
    'cbpo_lg_status': 'open',
        }
        
cbpo_lg()

class cbpo_lg_renew(osv.osv):
    _name = "cbpo.lg.renew"
    _description = "cbpo LG Renew Mangment"
    _columns = {
        'cbpo_lg_renew_id': fields.many2one('cbpo.lg', 'lg Reference', select=True, required=True, ondelete='cascade'),
        'cbpo_lg_renew_start_date': fields.date('Renew Start Date'),
        'cbpo_lg_renew_end_date': fields.date('Renew_end_date'),
		'cbpo_lg_renew_respon' : fields.many2one('hr.employee', 'Respon'),
        'cbpo_lg_renew_duration': fields.selection((('1','One Month'), ('3','Three Months'), ('6','Six Months'), ('9','Nine Months'), ('12','Year')),'Period'),
        'cbpo_lg_renew_note': fields.char('Note', size=128),
    }
cbpo_lg_renew()

class cbpo_lg_installment(osv.osv):
    _name = "cbpo.lg.installment"
    _description = "cbpo LG Installment Mangment"
    _columns = {
        'cbpo_lg_installment_id': fields.many2one('cbpo.lg', 'lg Reference2', select=True, required=True, ondelete='cascade'),
        'cbpo_lg_installment_date': fields.date('Installment Date'),
        'cbpo_lg_installment_amount': fields.integer('Installment Amount'),
        'cbpo_lg_installment_note': fields.char('Note', size=128),
    }
cbpo_lg_renew()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
