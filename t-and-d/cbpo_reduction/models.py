# -*- coding: utf-8 -*-

import time
from datetime import datetime
from openerp import models, fields, api
from openerp import SUPERUSER_ID
from openerp.exceptions import ValidationError
from openerp.tools.translate import _
from openerp.osv import osv
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class cbpoParamter(models.Model):
    _inherit = ['res.company']

    cbpo_reduction = fields.Float(string="Sales Reduction Limit")

    def percentageReduction(self, cr, uid, ids, cbpo_reduction, context=None):
        x = cbpo_reduction / 100
        return {'value': {'cbpo_reduction': x}}


class cbpoReduction(models.Model):
    _inherit = ['sale.order.line']

    @api.one
    def _calc(self):
        actualUnitPrice = self.cbpo_unit_price1
        changingUnitPrice = self.price_unit
        rec_company = self.env['res.company']
        findCompany = rec_company.search([('id', '=', self.order_id.company_id.id)])
        reduction = findCompany.cbpo_reduction
        # print '>>>>>>'
        # print (actualUnitPrice - (actualUnitPrice * reduction))
        if (actualUnitPrice - (actualUnitPrice * reduction)) > changingUnitPrice:
            self.cbpo_calc0 = True
        else:
            self.cbpo_calc0 = False

    cbpo_calc0 = fields.Boolean(compute='_calc', string='Calc')
