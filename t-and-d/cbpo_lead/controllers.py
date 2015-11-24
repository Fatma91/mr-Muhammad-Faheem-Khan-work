# -*- coding: utf-8 -*-
from openerp import http

# class CbpoLead(http.Controller):
#     @http.route('/cbpo_lead/cbpo_lead/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_lead/cbpo_lead/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_lead.listing', {
#             'root': '/cbpo_lead/cbpo_lead',
#             'objects': http.request.env['cbpo_lead.cbpo_lead'].search([]),
#         })

#     @http.route('/cbpo_lead/cbpo_lead/objects/<model("cbpo_lead.cbpo_lead"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_lead.object', {
#             'object': obj
#         })