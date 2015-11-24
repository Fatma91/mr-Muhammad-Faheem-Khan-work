# -*- coding: utf-8 -*-
from openerp import http

# class CbpoLegalInfoPartner(http.Controller):
#     @http.route('/cbpo_legal_info_partner/cbpo_legal_info_partner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_legal_info_partner/cbpo_legal_info_partner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_legal_info_partner.listing', {
#             'root': '/cbpo_legal_info_partner/cbpo_legal_info_partner',
#             'objects': http.request.env['cbpo_legal_info_partner.cbpo_legal_info_partner'].search([]),
#         })

#     @http.route('/cbpo_legal_info_partner/cbpo_legal_info_partner/objects/<model("cbpo_legal_info_partner.cbpo_legal_info_partner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_legal_info_partner.object', {
#             'object': obj
#         })