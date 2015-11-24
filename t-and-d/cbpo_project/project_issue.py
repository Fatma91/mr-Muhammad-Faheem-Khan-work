# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cbpo_project_issue(models.Model):
    _inherit = 'project.issue'

    cbpo_serial_no = fields.Char(string="Serial No.")
    cbpo_invoice_no = fields.Char(string="Invoice No.")
    cbpo_date = fields.Date(string="Date")