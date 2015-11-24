# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cbpoLead(models.Model):
    _inherit = ['crm.lead']


    partner_id = fields.Many2one('res.partner','Partner', ondelete='set null', track_visibility='onchange',
            select=True, help="Linked partner (optional). Usually created when converting the lead.",
            domain=[('is_company', '=', True),('parent_id', '=', None)])
    cbpo_contact_name = fields.Many2one("res.partner", 'Contact Name',)
    cbpo_potential_project = fields.Char('Potential Project')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=24, change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", 'State', ondelete='restrict')
    country_id = fields.Many2one('res.country', 'Country', ondelete='restrict')
    cbpo_stage_id = fields.Many2one('cbpo.stages', 'Project Stages')
    cbpo_item_id = fields.Many2many('product.category', string='Product Range',domain=[('parent_id', '=', False)])
    cbpo_estimate_id = fields.Many2many('cbpo.estimate', string='Estimated Project Size')
    contact_line = fields.One2many('cbpo.contact.opportunity', 'crm_lead_id', 'Contacts')
    cbpo_originator = fields.Many2one('res.partner', 'Originator',domain=[('is_company', '=', False),('parent_id', '=', None)])

    name_ = fields.Char('Name',required=True)
    cbpo_area = fields.Char('Area')
    cbpo_floors = fields.Char('Floors')
    cbpo_employees =fields.Many2one('res.users',string='Employees')
    cbpo_amount = fields.Char('Amount')
    cbpo_other = fields.Char('Other')
    cbpo_usd = fields.Many2one('res.currency',string='USD')

    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            if len(partner.child_ids) > 0:
                return {'domain': {'cbpo_contact_name': ['|',('id','in',partner.child_ids.ids)('cbpo_contact_name','=',False)]}}


    def onchange_contact_partner(self, cr, uid, id, cbpo_contact_name, context=None):
        values = {}
        if cbpo_contact_name:
            partner = self.pool.get('res.partner').browse(cr, uid, cbpo_contact_name, context=context)
            partner_name = (partner.parent_id and partner.parent_id.name) or (partner.is_company and partner.name) or False
            values = {
                'title': partner.title and partner.title.id or False,
                'street': partner.street,
                'street2': partner.street2,
                'city': partner.city,
                'state_id': partner.state_id and partner.state_id.id or False,
                'country_id': partner.country_id and partner.country_id.id or False,
                'email_from': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'fax': partner.fax,
                'zip': partner.zip,
                'function': partner.function,
            }
        return {'value': values}


class crm_case_section(models.Model):
    _inherit = ['crm.case.section']
    _description = "Sales Sector"


class cbpoStages(models.Model):
    _name = 'cbpo.stages'

    name = fields.Char(required=True)

class cbpoEstimate(models.Model):
    _name = 'cbpo.estimate'

    name = fields.Char('Name',required=True)
    cbpo_area = fields.Char('Area')
    cbpo_floors = fields.Char('Floors')
    cbpo_employees = fields.Char('Employees')
    cbpo_amount = fields.Char('Amount')
    cbpo_other = fields.Char('Other')


class cbpoContactOpportunity(models.Model):
    _name = 'cbpo.contact.opportunity'

    name = fields.Char()

    crm_lead_id = fields.Many2one('crm.lead', 'Project Stages')
    cbpo_contact = fields.Many2one('res.partner', 'Contact')
    cbpo_title = fields.Many2one('cbpo.project.role', 'Role to Project')
    cbpo_other = fields.Char('Notes')

class cbpoProjectRole(models.Model):
    _name = 'cbpo.project.role'

    name = fields.Char('Name',required=True)
