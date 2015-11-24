# -*- coding: utf-8 -*-
from openerp import http

# class CbpoProject(http.Controller):
#     @http.route('/cbpo_project/cbpo_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbpo_project/cbpo_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbpo_project.listing', {
#             'root': '/cbpo_project/cbpo_project',
#             'objects': http.request.env['cbpo_project.cbpo_project'].search([]),
#         })

#     @http.route('/cbpo_project/cbpo_project/objects/<model("cbpo_project.cbpo_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbpo_project.object', {
#             'object': obj
#         })