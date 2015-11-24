# -*- coding: utf-8 -*-
from openerp import http

# class CbpoCurrency(http.Controller):
#     @http.route('/cbpo_currency/cbpo_currency/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_currency/cbpo_currency/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_currency.listing', {
#             'root': '/cbpo_currency/cbpo_currency',
#             'objects': http.request.env['cbpo_currency.cbpo_currency'].search([]),
#         })

#     @http.route('/cbpo_currency/cbpo_currency/objects/<model("cbpo_currency.cbpo_currency"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_currency.object', {
#             'object': obj
#         })