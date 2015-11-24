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
from openerp.osv import fields, osv

class cbpo_tender(osv.osv):
    _name = "cbpo.tender"
    _description = "Cbpo Tender"
    _inhetit= 'res.partner'
    _rec_name = "cbpo_title"
    _columns = {
        'cbpo_title': fields.char('Subject', size=128),
        'cbpo_description': fields.text('Description'),
        'cbpo_deadline_tec_date': fields.date('Delivery date of the technical offer'),
        'cbpo_deadline_financial_date': fields.date('Delivery date of the financial offer'),
        'cbpo_due_tec_date': fields.date('Date of the technical decision'),
        'cbpo_due_financial_date': fields.date('Date of the financial decision'),
        'cbpo_start_date' : fields.date('Beginning of receipt'),
        'cbpo_specs_doc' : fields.boolean('Tender' ),
        'cbpo_fees': fields.integer('Tender Measuring'),
        'cbpo_lg': fields.boolean('Letters of guarantee required'),
        'cbpo_lg_value': fields.integer('The value of the letter of guarantee'),
        'cbpo_lg_duration' : fields.selection((('1','One Month'), ('3','Three Months'), ('6','Six Months')),'Period letter of guarantee'),
        'cbpo_type' : fields.selection((('tender','Tender'), ('practices','Practices')),'Type'),
        'cbpo_direction': fields.selection((('in','purchase'), ('out','sales')),'Case' ),
        'cbpo_scope' : fields.selection((('open','Open'), ('close','Close'),('limited','Limited')),'Type' ),
        'cbpo_advs' : fields.text('The announcement of the tender data'),
        # 'cbpo_communty_members' : fields.many2many('hr.employee','cbpo_tender_hr','cbpo_tender_id', 'user_id', 'اعضاء اللجنة'),
        # 'cbpo_partner' : fields.many2many('res.partner', 'parent_id', 'المشاركون'),
    }
        
    _defaults = {
    'cbpo_start_date':  fields.datetime.now,
    'cbpo_type': 'tender',
        }
        
cbpo_tender()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
