# -*- coding: utf-8 -*-

# from openerp import models, fields, api

#
# class hr_fingerprint_data(models.Model):
#     _name = "hr.fingerprint_data"
#     _inherit = ['ir.needaction_mixin']
#     _description = "fingerprint data Attendance .. "
#
#
#     name = fields.Datetime(string="DateTime", required=False, )
#
#     action = fields.Char(string="action", required=False, )
#     compute = fields.Char(string="compute", default="0" ,  required=False, )
#     fid = fields.Integer(string="Finger ID",  required=True, )
#
#
#
#     def _needaction_domain_get(self   , cr, uid , context=None):
#
#         """
#         Show a count of sick horses on the menu badge.
#         An exception: don't show the count to Bob,
#         because he worries too much!
#         """
#         # if self.env.user.name == "Bob":
#         #     return False  # don't show to Bob!
#         return [('compute', '=', '0')]


#
#
# class print_report_att2(models.AbstractModel):
#     _name = 'report.cbpo_hr_attend_new.report_attendance2_1'
#     @api.multi
#     def render_html(self, data):
#
#
#         report_obj = self.env['report']
#         report = report_obj._get_report_from_name('cbpo_hr_attend_new.report_attendance2_1')
#         docargs = {
#             'doc_ids': self._ids,
#             'doc_model': report.model,
#             'docs': self,
#             'employee': data[0],
#             'day_from': data[1],
#             'day_to': data[2],
#
#         }
#         return report_obj.render('cbpo_hr_attend_new.report_attendance2_1', docargs)

    # def print_quotation(self, cr, uid, ids, context=None):
    #     '''
    #     This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
    #     '''
    #     assert len(ids) == 1, 'This option should only be used for a single id at a time'
    #     self.signal_workflow(cr, uid, ids, 'quotation_sent')
    #     return self.pool['report'].get_action(cr, uid, ids, 'sale.report_saleorder', context=context)


