# -*- coding: utf-8 -*-
from openerp import http

# class CbpoReduction(http.Controller):
#     @http.route('/cbpo_reduction/cbpo_reduction/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_reduction/cbpo_reduction/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_reduction.listing', {
#             'root': '/cbpo_reduction/cbpo_reduction',
#             'objects': http.request.env['cbpo_reduction.cbpo_reduction'].search([]),
#         })

#     @http.route('/cbpo_reduction/cbpo_reduction/objects/<model("cbpo_reduction.cbpo_reduction"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_reduction.object', {
#             'object': obj
#         })