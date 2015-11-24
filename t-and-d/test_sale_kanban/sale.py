# -*- coding: utf-8 -*-
from openerp import fields, models

class sale_order(models.Model):
        _inherit = 'sale.order'
        color = fields.Integer()