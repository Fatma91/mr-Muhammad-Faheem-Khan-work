# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from openerp import exceptions
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP


class PurchaseConfirmationWizard(models.TransientModel):
    _name = "purchase.confirmation.wizard"
    _description = "purchase.confirmation.wizard"

    name = fields.Char()
    partner_id = fields.Many2one('res.partner', string='Supplier', required=True, change_default=True, track_visibility='always')
    # purchase_wizard_ids = fields.One2many('purchase.wizard.line', 'purchase_wizard_id', string="Line")


    @api.multi
    def product_compute(self):
        self.ensure_one()
        context = self._context
        purchase = self.env['purchase.order']
        purchase_line = self.env['purchase.order.line']
        pricelist_partnerinfo = self.env['pricelist.partnerinfo']
        product_supplierinfo = self.env['product.supplierinfo']
        all_product = purchase_line.search([('cbpo_select_line', '=', True)])
        all_purchase = purchase.search([('order_line', 'in', all_product.ids)])
        for line1 in purchase.browse(all_purchase.ids):
            poid = purchase.create({
                                    'partner_id': self.partner_id.id,
                                    'picking_type_id': 1,
                                    'location_id': 12,
                                    'pricelist_id': 2,
                                    'origin': line1.origin,
                                    })
            supplierinfo = False
            for line2 in purchase_line.browse(all_product.ids):
                for y in line2.product_id.product_tmpl_id.seller_ids:
                    if line2.product_id.product_tmpl_id.seller_ids.name.id and (y.name.id == line2.product_id.product_tmpl_id.seller_ids.name.id):
                        supplierinfo = y
                val1 = product_supplierinfo.browse(line2.product_id.product_tmpl_id.seller_ids.name.id)
                rec2 = pricelist_partnerinfo.search([('suppinfo_id', '=', val1.id)])
                val2 = pricelist_partnerinfo.browse(rec2)
                dplan = purchase_line._get_date_planned(supplierinfo,line1.date_order).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                purchase_line.create({'cbpo_client_code': line2.cbpo_client_code,
                                                                          'cbpo_partner_id': line2.cbpo_partner_id,
                                                                          'cbpo_area': line2.cbpo_area,
                                                                          'cbpo_floor': line2.cbpo_floor,
                                                                          'item_name': line2.item_name.id,
                                                                          'product_id': line2.product_id.id,
                                                                          'cbpo_supplier': line2.cbpo_supplier,
                                                                          'cbpo_supplier_item_code': line2.cbpo_supplier_item_code,
                                                                          'cbpo_finishes': line2.cbpo_finishes.id,
                                                                          'account_analytic_id': line2.account_analytic_id.id,
                                                                          'name': line2.name,
                                                                          'product_qty': line2.product_qty,
                                                                          'price_unit': line2.price_unit,
                                                                          'order_id': poid.id,
                                                                          'product_uom': line2.product_uom.id,
                                                                          'date_planned': dplan,
                                                                          })
            purchase_line.search([('cbpo_select_line', '=', True)]).unlink()

            # return {
            #     'name': title,
            #     'view_type': 'form',
            #     'view_mode': 'tree,form',
            #     'res_model': 'account.move',
            #     'view_id': False,
            #     'domain': "[('id','in',["+','.join(map(str, created_move_ids))+"])]",
            #     'type': 'ir.actions.act_window',
            # }


# class PurchaseWizardLine(models.TransientModel):
#     _name = "purchase.wizard.line"
#     _description = "purchase.wizard.line"
#
#     name = fields.Char()
#     purchase_wizard_id = fields.Many2one('purchase.confirmation.wizard')
#     product_id = fields.Many2one('product.product', string='Product',required=True)
