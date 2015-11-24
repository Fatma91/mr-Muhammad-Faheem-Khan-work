# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cbpo_project_project(models.Model):
    _inherit = 'project.project'

    @api.one
    def _cbpo_type_ref(self):
        sale_order = self.env['sale.order']
        sale_projec_id = sale_order.search([('project_id', '=', self.analytic_account_id.id)])
        if len(sale_projec_id) > 0:
            type_id = sale_order.browse(sale_projec_id[0].id)
            if type_id.cbpo_type == 'O':
                self.cbpo_type_ref = "Office"
            elif type_id.cbpo_type == 'K':
                self.cbpo_type_ref = "Kitchen"
            elif type_id.cbpo_type == 'H':
                self.cbpo_type_ref = "Home"

    cbpo_type_ref = fields.Char(compute='_cbpo_type_ref', string="Type")