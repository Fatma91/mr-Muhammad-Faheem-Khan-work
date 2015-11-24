# -*- coding: utf-8 -*-
from openerp import http

# class CbpoHr(http.Controller):
#     @http.route('/cbpo_hr/cbpo_hr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_hr/cbpo_hr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_hr.listing', {
#             'root': '/cbpo_hr/cbpo_hr',
#             'objects': http.request.env['cbpo_hr.cbpo_hr'].search([]),
#         })

#     @http.route('/cbpo_hr/cbpo_hr/objects/<model("cbpo_hr.cbpo_hr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_hr.object', {
#             'object': obj
#         })