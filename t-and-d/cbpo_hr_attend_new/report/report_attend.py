#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv
from openerp.report import report_sxw


class attendance2_report_1(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(attendance2_report_1, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_attendance2_report_1': self.get_attendance2_report_1,


        })

    def get_attendance2_report_1(self):


        # def  get_details_by_rule_category2(self, obj,currency_id):
        # payslip_line = self.pool.get('hr.payslip.line')
        # rule_cate_obj = self.pool.get('hr.salary.rule.category')
        # currency_obj = self.pool.get('res.currency').browse(self.cr, self.uid, [currency_id])
        # currency_rate=currency_obj.rate_silent

        # def get_recursive_parent2(rule_categories):
        #     if not rule_categories:
        #         return []
        #     if rule_categories[0].parent_id:
        #         rule_categories.insert(0, rule_categories[0].parent_id)
        #         get_recursive_parent2(rule_categories)
        #     return rule_categories

        res = []
        result = {}
        ids = []

        # for id in range(len(obj)):
        #     ids.append(obj[id].id)
        # if ids:
        #     self.cr.execute('''SELECT pl.id, pl.category_id FROM hr_payslip_line as pl \
        #         LEFT JOIN hr_salary_rule_category AS rc on (pl.category_id = rc.id) \
        #         WHERE pl.id in %s \
        #         GROUP BY rc.parent_id, pl.sequence, pl.id, pl.category_id \
        #         ORDER BY pl.sequence, rc.parent_id''',(tuple(ids),))
        #     for x in self.cr.fetchall():
        #         result.setdefault(x[1], [])
        #         result[x[1]].append(x[0])
        #     for key, value in result.iteritems():
        #         rule_categories = rule_cate_obj.browse(self.cr, self.uid, [key])
        #         parents = get_recursive_parent2(rule_categories)
        #         category_total = 0
        #         for line in payslip_line.browse(self.cr, self.uid, value):
        #             category_total += line.total
        #         level = 0
        #
        res.append({
                        'a': 'aa_1',
                        'b': 'bb_1',
                        'c': 'cc_1',


                    })

        res.append({
                        'a': 'aa_2',
                        'b': 'bb_2',
                        'c': 'cc_2',


                    })
        return res



class wrapped_report_attendance2_report_1(osv.AbstractModel):
    _name = 'report.cbpo_hr_attend_new.report_attendance2_1'
    # _inherit = 'report.hr_payroll.report_payslipdetails'
    _inherit = 'report.abstract_report'
    # _template = 'hr_payroll.report_payslipdetails2'
    _template = 'cbpo_hr_attend_new.report_attendance2_1'
    _wrapped_report_class = attendance2_report_1

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
