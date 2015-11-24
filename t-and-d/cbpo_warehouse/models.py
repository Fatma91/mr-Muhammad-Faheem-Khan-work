    # -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class cbpoWarehouseDate(models.Model):
    _inherit = 'stock.picking'

    @api.one
    def _compute_amount(self):

        model = self.env['stock.picking']
        c_ids=model.search(['&','&',('id' , '>' , 0),('picking_type_id.code','=','incoming'),('cbpo_act_amount','!=',0.0)])
        total_amount = 0.0
        # res = self.browse(cr, uid, ids, context=context)
        for record in c_ids:
            total_amount += record.cbpo_act_amount
        total  =len(c_ids)
        if total > 0 :
            self.cbpo_exp_cheque_amount = total_amount / total
        else:
            self.cbpo_exp_cheque_amount = 0.0

    picking_type_code = fields.Selection([('incoming', 'Suppliers'), ('outgoing', 'Customers'), ('internal', 'Internal')], related='picking_type_id.code', store=True )
    cbpo_req_pick = fields.Date('Request for Pick up')
    cbpo_act_pick = fields.Date('Actual Pick up')
    cbpo_exp_dep = fields.Date('Expected Departure')
    cbpo_act_dep = fields.Date('Actual Departure')
    cbpo_exp_arr = fields.Date('Expected Arrival')
    cbpo_act_arr = fields.Date('Actual Arrival')
    cbpo_date_rec_ship_doc = fields.Date('Date of Receiving shipping docs')
    cbpo_send_doc_account = fields.Date('Send Docs to Accountant')
    cbpo_send_4_doc = fields.Date('Send Form.4 Docs to Bank')
    cbpo_4_issue = fields.Date('Form.4 Issue from Bank')
    cbpo_send_doc_clear = fields.Date('Send Docs to Clearer')
    cbpo_clear_star = fields.Date('Clearer starting work')
    cbpo_ship_release = fields.Date('Shipment release date')
    cbpo_delivery_cust = fields.Date('Delivery to Customer')

    cbpo_exp_cheque_amount = fields.Float(string="Expected Cheque Amount", compute='_compute_amount')
    cbpo_clear_exp = fields.Float(string="Clear's Expectation")
    cbpo_act_amount = fields.Float(string="Actual Amount")