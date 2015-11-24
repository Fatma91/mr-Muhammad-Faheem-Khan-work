# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields, osv


class update_crm_lead(osv.osv):
    _inherit = 'crm.lead'

    _columns = {
        'cbpo_other_contacts1': fields.char('Other Contacts'),
        'cbpo_other_contacts2': fields.char('.'),
        'cbpo_web_site': fields.char('Web Site' ),
    }


update_crm_lead()


