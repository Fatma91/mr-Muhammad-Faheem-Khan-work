# -*- coding: utf-8 -*-

from openerp import models, fields, api


import datetime
import math
import time
from operator import attrgetter

from openerp.exceptions import Warning
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _


class hr_holidays2(models.Model):
    # _name = 'new_module.new_module'
    _inherit = 'hr.holidays'


    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('state') and vals['state'] not in ['draft', 'confirm', 'cancel'] and not self.pool['res.users'].has_group(cr, uid, 'base.group_hr_user') and not self.pool['res.users'].has_group(cr, uid, 'cbpo_hr_holidays.group_hr_manger_holidays'):
            raise osv.except_osv(_('Warning!'), _('You cannot set a leave request as \'%s\'. Contact a human resource manager.') % vals.get('state'))
        return super(hr_holidays2, self).write(cr, uid, ids, vals, context=context)
