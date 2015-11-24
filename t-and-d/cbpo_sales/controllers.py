# -*- coding: utf-8 -*-
from openerp import http

# class CbpoSales(http.Controller):
#     @http.route('/cbpo_sales/cbpo_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_sales/cbpo_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_sales.listing', {
#             'root': '/cbpo_sales/cbpo_sales',
#             'objects': http.request.env['cbpo_sales.cbpo_sales'].search([]),
#         })

#     @http.route('/cbpo_sales/cbpo_sales/objects/<model("cbpo_sales.cbpo_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_sales.object', {
#             'object': obj
#         })