# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import osv

class cbpo_project_task(models.Model):
    _inherit = 'project.task'

    sale_id = fields.Many2one('sale.order', 'Sale Order')
    an_account_id = fields.Many2one('account.analytic.account', string="an_account",related='project_id.analytic_account_id', store=True,)
    # analytic_account_id = fields.Integer(related="project_id.analytic_account_id.id", string="analytic_account",store=True, readonly=True)
    # fields.Many2one('res.partner', string='Partner',
    #     related='invoice_id.partner_id', store=True, readonly=True)



    # def onchange_member(self, cr, uid, id, project_id, context=None):
    #     sale_order = self.pool.get('sale.order')
    #     sale_order_line = self.pool.get('sale.order.line')
    #     sale_projec_id = sale_order.search(cr, uid,[('project_id', '=', project_id)])
    #     if len(sale_projec_id) > 0:
    #         sale_line = sale_order.browse(cr, uid, sale_projec_id[0].id)
    #     return {'value': {'sale_id': sale_line.id}}

    def onchange_project(self, cr, uid, id, project_id, context=None):
        if project_id:
            project = self.pool.get('project.project').browse(cr, uid, project_id, context=context)
            sale_order = self.pool.get('sale.order')
            sale_order_line = self.pool.get('sale.order.line')
            sale_projec_id = sale_order.search(cr, uid,[('project_id', '=', project.analytic_account_id.id)])
            sale_line = {}
            if len(sale_projec_id) > 0:
                sale_line = sale_order.browse(cr, uid, sale_projec_id[0])
            if project and project.partner_id:
                return {'value': {'partner_id': project.partner_id.id,'sale_id': sale_line.id}}
        return {}


class cbpo_project_task_work(models.Model):
    _inherit = 'project.task.work'

    sale_line_id = fields.Many2one('sale.order.line', 'Product',)
    product_qty = fields.Float(string="Quantity", related='sale_line_id.product_uom_qty', store=True)
    planned_qty = fields.Float('Planned Quantity')
    planned_duration = fields.Date('Planned Duration')
    qty_done = fields.Float('Quantity Done')
    all_befor_time = fields.Date('All Before Time Spend')
    planned_start = fields.Date('Planned Start')

    def get_work_members(self, cr, uid, ids, sale_line_id, context=None):
        lids =[]
        if sale_line_id:
            project_my = self.pool.get('project.project')
            sale_order_line = self.pool.get('sale.order.line')
            sale_line = sale_order_line.browse(cr, uid, sale_line_id)
            project_id = project_my.search(cr, uid,[('analytic_account_id', '=', sale_line.order_id.project_id.id)])
            project_member = project_my.browse(cr, uid, project_id)
            return {'domain': {'user_id': [('id','in',project_member.members.ids)]}}


class hr_holidayss(models.Model):
    _inherit = ['hr.attendance', 'ir.needaction_mixin']

    def _needaction_domain_get(self, cr, uid, context=None):
        # emp_obj = self.pool.get('hr.employee')
        # empids = emp_obj.search(cr, uid, [('parent_id.user_id', '=', uid)], context=context)
        # dom = ['&', ('state', '=', 'confirm'), ('employee_id', 'in', empids)]
        # # if this user is a hr.manager, he should do second validations
        # if self.pool.get('res.users').has_group(cr, uid, 'base.group_hr_manager'):
        #     dom = ['|'] + dom + [('state', '=', 'validate1')]
        return  [('action', '=', 'sgin_in')]
