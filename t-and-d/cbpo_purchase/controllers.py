# -*- coding: utf-8 -*-
from openerp import http

# class CbpoPurchase(http.Controller):
#     @http.route('/cbpo_purchase/cbpo_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_purchase/cbpo_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_purchase.listing', {
#             'root': '/cbpo_purchase/cbpo_purchase',
#             'objects': http.request.env['cbpo_purchase.cbpo_purchase'].search([]),
#         })

#     @http.route('/cbpo_purchase/cbpo_purchase/objects/<model("cbpo_purchase.cbpo_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_purchase.object', {
#             'object': obj
#         })