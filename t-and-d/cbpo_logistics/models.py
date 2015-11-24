# -*- coding: utf-8 -*-

from openerp import models, fields, api


class purchase_logistics(models.Model):
    _inherit = 'purchase.order'


class sales_logistics(models.Model):
    _inherit = 'sale.order'


class warehouse_logistics(models.Model):
    _inherit = 'stock.picking'
