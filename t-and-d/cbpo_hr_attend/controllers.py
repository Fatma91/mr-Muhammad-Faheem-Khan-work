# -*- coding: utf-8 -*-
from openerp import http

# class CbpoHrAttend/(http.Controller):
#     @http.route('/cbpo_hr_attend//cbpo_hr_attend//', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_hr_attend//cbpo_hr_attend//objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_hr_attend/.listing', {
#             'root': '/cbpo_hr_attend//cbpo_hr_attend/',
#             'objects': http.request.env['cbpo_hr_attend/.cbpo_hr_attend/'].search([]),
#         })

#     @http.route('/cbpo_hr_attend//cbpo_hr_attend//objects/<model("cbpo_hr_attend/.cbpo_hr_attend/"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_hr_attend/.object', {
#             'object': obj
#         })