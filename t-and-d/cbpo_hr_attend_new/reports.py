# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class cbpo_hr_attend/(models.Model):
#     _name = 'cbpo_hr_attend/.cbpo_hr_attend/'

#     name = fields.Char()



class my_reports(models.AbstractModel):
    _name = 'report.cbpo_hr_attend_new.report_hr_attendance_test_template'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('cbpo_hr_attend_new.report_hr_attendance_test_template')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,

        }
        return report_obj.render('cbpo_hr_attend_new.report_hr_attendance_test_template', docargs)