# -*- coding: utf-8 -*-

from openerp import models, fields, api


class cbpo_legal_info_partner(models.Model):
    _inherit = 'res.partner'

    cbpo_name = fields.Char(string="Legal Name", size=128, select=True)
    cbpo_legal_crn = fields.Char(string="Commercial Register No.", size=128)
    cbpo_legal_issued1 = fields.Date(string="Issuance Date")
    cbpo_legal_inno = fields.Char(string="Insurance No.", size=128)
    cbpo_legal_tcn = fields.Char(string="Tax Card No.", size=128)
    cbpo_legal_issued2 = fields.Date(string="Issurance Date")
    cbpo_legal_tfn = fields.Char(string="Tax File No.", size=128)
    cbpo_legal_to = fields.Char(string="Tax Office", size=128)
    competitor = fields.Boolean(string='Competitor', help="Check this box if this contact is a competitor.")
    # HAZEM
    cbpo_guarantee = fields.Float(string="Guarantee")
    cbpo_supplier_discount = fields.Float(string="Supplier Discount")
    cbpo_production_time_stand = fields.Float(string="Production Time")
    cbpo_shipping_time_stand = fields.Float(string="Shipping Time")
    cbpo_clearance_stand = fields.Float(string="Duty Clearance")
    cbpo_production_time_non_stand = fields.Float(string="Production Time")
    cbpo_shipping_time_non_stand = fields.Float(string="Shipping Time")
    cbpo_clearance_non_stand = fields.Float(string="Duty Clearance")
