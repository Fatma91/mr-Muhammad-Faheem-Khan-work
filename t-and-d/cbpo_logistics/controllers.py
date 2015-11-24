# -*- coding: utf-8 -*-
from openerp import http

# class CbpoLogistics(http.Controller):
#     @http.route('/cbpo_logistics/cbpo_logistics/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_logistics/cbpo_logistics/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_logistics.listing', {
#             'root': '/cbpo_logistics/cbpo_logistics',
#             'objects': http.request.env['cbpo_logistics.cbpo_logistics'].search([]),
#         })

#     @http.route('/cbpo_logistics/cbpo_logistics/objects/<model("cbpo_logistics.cbpo_logistics"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_logistics.object', {
#             'object': obj
#         })