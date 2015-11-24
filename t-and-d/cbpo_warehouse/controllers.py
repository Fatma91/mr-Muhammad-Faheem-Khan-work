# -*- coding: utf-8 -*-
from openerp import http

# class CbpoWarehouse(http.Controller):
#     @http.route('/cbpo_warehouse/cbpo_warehouse/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_warehouse/cbpo_warehouse/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_warehouse.listing', {
#             'root': '/cbpo_warehouse/cbpo_warehouse',
#             'objects': http.request.env['cbpo_warehouse.cbpo_warehouse'].search([]),
#         })

#     @http.route('/cbpo_warehouse/cbpo_warehouse/objects/<model("cbpo_warehouse.cbpo_warehouse"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_warehouse.object', {
#             'object': obj
#         })