# -*- coding: utf-8 -*-
from openerp import http

# class CbpoCustomerInvoice(http.Controller):
#     @http.route('/cbpo_customer_invoice/cbpo_customer_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_customer_invoice/cbpo_customer_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_customer_invoice.listing', {
#             'root': '/cbpo_customer_invoice/cbpo_customer_invoice',
#             'objects': http.request.env['cbpo_customer_invoice.cbpo_customer_invoice'].search([]),
#         })

#     @http.route('/cbpo_customer_invoice/cbpo_customer_invoice/objects/<model("cbpo_customer_invoice.cbpo_customer_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_customer_invoice.object', {
#             'object': obj
#         })