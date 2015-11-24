# -*- coding: utf-8 -*-


from openerp import models, fields, api, exceptions, _

class cbpo_customer_invoice(models.Model):
    _inherit = 'account.invoice'

    account_analytic_id = fields.Many2one('account.analytic.account',string='Project name')



    def onchange_analytic_id(self, cr, uid, ids, account_analytic_id, context=None):
        res = {}
        val0 = self.read(cr, uid, ids, ['invoice_line'])
        for line in self.browse(cr, uid, ids, context=context):
            val = line.invoice_line
            val2 = []
            if not val:
                pass

            else:
                for line1 in val0[0]['invoice_line']:
                    val1 = self.pool.get('account.invoice.line').search(cr, uid, [('id', '=', line1)])
                    self.pool.get('account.invoice.line').write(cr, uid, val1, { 'account_analytic_id': account_analytic_id})

        return res


class cbpo_customer_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    customer_code = fields.Char('Customer Code')
    supplier_code = fields.Char('Supplier Code')