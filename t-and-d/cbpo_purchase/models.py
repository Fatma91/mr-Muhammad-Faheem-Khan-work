# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp import netsvc
from openerp import SUPERUSER_ID, workflow
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.osv.orm import browse_record_list, browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools.float_utils import float_compare


class cbpo_sale_order_to_purchase_order(models.Model):
    _inherit = 'sale.order'



    def action_to_purchase(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        # add Task 1 Code
        # val0 = self.pool.get('sale.order.line').search(cr, uid, [('invoice_ids','in', ids)])
        results = self.read(cr, uid, ids, ['name', 'order_line', 'date_order'])

        for x in results[0]['order_line']:
            purchase_order_line = self.pool.get('purchase.order.line')
            sale_order_line = self.pool.get('sale.order.line')
            val = sale_order_line.browse(cr, uid, x)
            product_product = self.pool.get('product.product')
            pricelist_partnerinfo = self.pool.get('pricelist.partnerinfo')
            product_supplierinfo = self.pool.get('product.supplierinfo')
            if not self.pool.get('purchase.order').search(cr, uid, ['&', (
                    'partner_id', '=', val.product_id.product_tmpl_id.seller_ids.name.id),
                                                                    ('origin', '=', val.order_id.name)]):
                poid = self.pool.get('purchase.order').create(cr, uid, {
                    'partner_id': val.product_id.product_tmpl_id.seller_ids.name.id,
                    'picking_type_id': 1,
                    'location_id': 12,
                    'pricelist_id': 2,
                    'origin': results[0]['name'],
                })
            else:
                pass
            supplierinfo = False
            for y in val.product_id.product_tmpl_id.seller_ids:
                if val.product_id.product_tmpl_id.seller_ids.name.id and (
                            y.name.id == val.product_id.product_tmpl_id.seller_ids.name.id):
                    supplierinfo = y
            val1 = product_supplierinfo.browse(cr, uid, val.product_id.product_tmpl_id.seller_ids.name.id)
            rec2 = pricelist_partnerinfo.search(cr, uid, [('suppinfo_id', '=', val1.id)])
            val2 = pricelist_partnerinfo.browse(cr, uid, rec2)
            dplan = purchase_order_line._get_date_planned(cr, uid, supplierinfo, results[0]['date_order']).strftime(
                DEFAULT_SERVER_DATETIME_FORMAT)
            if not self.pool.get('purchase.order.line').search(cr, uid,
                                                               ['&', ('order_id.partner_id', '=',
                                                                      val.product_id.product_tmpl_id.seller_ids.name.id),
                                                                ('order_id.origin', '=', val.order_id.name)]) and val.product_id.product_tmpl_id.type != 'service':
                self.pool.get('purchase.order.line').create(cr, uid, {'cbpo_client_code': val.cbpo_client_code,
                                                                      'cbpo_partner_id': val.order_id.partner_id.id,
                                                                      'cbpo_area': val.cbpo_area,
                                                                      'cbpo_floor': val.cbpo_floor,
                                                                      'item_name': val.item_name.id,
                                                                      'product_id': val.product_id.id,
                                                                      'cbpo_supplier': val.cbpo_supplier,
                                                                      'cbpo_supplier_item_code': val.cbpo_supplier_item_code,
                                                                      'cbpo_finishes': val.cbpo_finishes.id,
                                                                      'account_analytic_id': val.order_id.project_id.id,
                                                                      'name': val.name,
                                                                      'order_line_id': val.id,
                                                                      'product_qty': val.product_uom_qty,
                                                                      'price_unit': val.product_id.product_tmpl_id.seller_ids.cbpo_after_unit_price,
                                                                      'order_id': poid,
                                                                      'product_uom': val.product_uom.id,
                                                                      'date_planned': dplan,
                                                                      })
            else:
                pass

        # add Task 1 Code Code

        return True


class cbpo_sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    order_supplier_id = fields.Many2one(comodel_name="res.partner", string="Supplier", required=False,
                                        domain=[('supplier', '=', True)])


class cbpo_purchese_order(models.Model):
    _inherit = 'purchase.order'

    @api.one
    def _client_order_ref(self):
        sale = self.env['sale.order']
        sale_id = sale.search([('name', '=', self.origin)])
        for sale_rec in sale.browse(sale_id.ids):
            self.cbpo_client_order_ref = sale_rec.cbpo_client_order_ref

    @api.one
    def _date_of_delivery(self):
        dateList = []
        for line in self.order_line:
            dateList.append(line.date_planned)
            self.cbpo_date_of_delivery = max(dateList)

    cbpo_proforma_invoice_no = fields.Char(string="Proforma invoice No.")
    cbpo_proforma_invoice_date = fields.Date(string="Proforma invoice date")
    cbpo_proforma_receiving_date = fields.Date(string="Proforma Receiving date")
    cbpo_proforma_sending_to_accountant = fields.Date(string="Proforma sending to accountant")
    cbpo_date_of_down_payment = fields.Date(string="Date of down payment")
    cbpo_date_of_second_payment = fields.Date(string="Date of Second payment")
    cbpo_manufacturing_date = fields.Date(string="Manufacturing date")
    cbpo_date_of_delivery = fields.Date(string="Date of Delivery",compute='_date_of_delivery',)
    cbpo_duration_of_manufacturing = fields.Date(string="Duration of Manufacturing")
    cbpo_duration_of_cusrom_manuf = fields.Date(string="Duration of Customized Manufacturing")
    cbpo_commercial_invoice = fields.Boolean(string="Commercial invoice")
    cbpo_eur = fields.Boolean(string="EUR")
    cbpo_packing_list = fields.Boolean(string="Packing list")
    cbpo_waybill = fields.Boolean(string="Waybill")
    cbpo_bill_o_landing = fields.Boolean(string="Bill of Landing")
    cbpo_flight_invoice = fields.Boolean(string="Flight Invoice")
    cbpo_certificate_o_origin = fields.Boolean(string="Certificate of Origin")
    cbpo_type = fields.Many2one('product.category',string="Product Range",domain=[('parent_id', '=', False)])
    cbpo_delivery_term = fields.Many2one('cbpo.delivery.term', string="Delivery Term")
    cbpo_client_order_ref = fields.Char(string="SO Ref.",compute='_client_order_ref',)
    state = fields.Selection(selection=[('draft', 'Draft PO'),
                                        ('revised', 'Reviseded'),
                                        ('sent', 'RFQ'),
                                        ('bid', 'Bid Received'),
                                        ('confirmed', 'Waiting Approval'),
                                        ('approved', 'Purchase Confirmed'),
                                        ('except_picking', 'Shipping Exception'),
                                        ('except_invoice', 'Invoice Exception'),
                                        ('done', 'Done'),
                                        ('cancel', 'Cancelled')],
                                        string="Status",readonly=True,
                                        help="The status of the purchase order or the quotation request. "
                                       "A request for quotation is a purchase order in a 'Draft' status. "
                                       "Then the order has to be confirmed by the user, the status switch "
                                       "to 'Confirmed'. Then the supplier must confirm the order to change "
                                       "the status to 'Approved'. When the purchase order is paid and "
                                       "received, the status becomes 'Done'. If a cancel action occurs in "
                                       "the invoice or in the receipt of goods, the status becomes "
                                       "in exception.",
                                        select=True, copy=False)


    def revised_cancel(self, cr, uid, ids, context=None):
        if not len(ids):
            return False
        self.write(cr, uid, ids, {'state':'draft','shipped':0})
        self.set_order_line_status(cr, uid, ids, 'draft', context=context)
        for p_id in ids:
            # Deleting the existing instance of workflow for PO
            self.delete_workflow(cr, uid, [p_id]) # TODO is it necessary to interleave the calls?
            self.create_workflow(cr, uid, [p_id])
            self.write(cr, uid, ids, {'state': 'revised'})
        return True


class cbpo_purchese_order_line(models.Model):
    _inherit = 'purchase.order.line'

    # @api.one
    # def _price_unit(self):
    #     self.price_unit = self.product_id.product_tmpl_id.seller_ids.cbpo_after_unit_price
    #
    # price_unit = fields.Float(compute='_price_unit', required=False)
    cbpo_product_category = fields.Many2one('product.category',string="Product Category")
    cbpo_line_category = fields.Many2one(comodel_name='product.category',string="Product Type",)
    order_line_id = fields.Many2one(comodel_name="sale.order.line", string="Line", required=False, )
    cbpo_partner_id = fields.Char(comodel_name="res.partner", string="Client")
    cbpo_client_code = fields.Char(string="Client code")
    cbpo_floor = fields.Char(string="Floor")
    cbpo_area = fields.Char(string="Area")
    item_name = fields.Many2one('item.name', string="Item Name")
    cbpo_supplier = fields.Char(string="Supplier", )
    cbpo_supplier_item_code = fields.Char(related='product_id.product_tmpl_id.seller_ids.product_code', string="Supplier Item Code")
    cbpo_finishes = fields.Many2one('cbpo.product.attribute', string="Finishes", )
    cbpo_comments = fields.Text(string="Comments")
    cbpo_select_line = fields.Boolean(string="Select Product")

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None):
        """
        onchange handler of product_id.
        """
        if context is None:
            context = {}

        res = {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'product_uom' : uom_id or False}}
        if not product_id:
            if not uom_id:
                uom_id = self.default_get(cr, uid, ['product_uom'], context=context).get('product_uom', False)
                res['value']['product_uom'] = uom_id
            return res

        product_product = self.pool.get('product.product')
        product_uom = self.pool.get('product.uom')
        res_partner = self.pool.get('res.partner')
        product_pricelist = self.pool.get('product.pricelist')
        account_fiscal_position = self.pool.get('account.fiscal.position')
        account_tax = self.pool.get('account.tax')

        # - check for the presence of partner_id and pricelist_id
        #if not partner_id:
        #    raise osv.except_osv(_('No Partner!'), _('Select a partner in purchase order to choose a product.'))
        #if not pricelist_id:
        #    raise osv.except_osv(_('No Pricelist !'), _('Select a price list in the purchase order form before choosing a product.'))

        # - determine name and notes based on product in partner lang.
        context_partner = context.copy()
        if partner_id:
            lang = res_partner.browse(cr, uid, partner_id).lang
            context_partner.update( {'lang': lang, 'partner_id': partner_id} )
        product = product_product.browse(cr, uid, product_id, context=context_partner)
        #call name_get() with partner in the context to eventually match name and description in the seller_ids field
        if not name or not uom_id:
            # The 'or not uom_id' part of the above condition can be removed in master. See commit message of the rev. introducing this line.
            dummy, name = product_product.name_get(cr, uid, product_id, context=context_partner)[0]
            if product.description_purchase:
                name += '\n' + product.description_purchase
            res['value'].update({'name': name})

        # - set a domain on product_uom
        res['domain'] = {'product_uom': [('category_id','=',product.uom_id.category_id.id)]}

        # - check that uom and product uom belong to the same category
        product_uom_po_id = product.uom_po_id.id
        if not uom_id:
            uom_id = product_uom_po_id

        if product.uom_id.category_id.id != product_uom.browse(cr, uid, uom_id, context=context).category_id.id:
            if context.get('purchase_uom_check') and self._check_product_uom_group(cr, uid, context=context):
                res['warning'] = {'title': _('Warning!'), 'message': _('Selected Unit of Measure does not belong to the same category as the product Unit of Measure.')}
            uom_id = product_uom_po_id

        res['value'].update({'product_uom': uom_id})

        # - determine product_qty and date_planned based on seller info
        if not date_order:
            date_order = fields.datetime.now()


        supplierinfo = False
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Unit of Measure')
        for supplier in product.seller_ids:
            if partner_id and (supplier.name.id == partner_id):
                supplierinfo = supplier
                if supplierinfo.product_uom.id != uom_id:
                    res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
                min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=uom_id)
                if float_compare(min_qty , qty, precision_digits=precision) == 1: # If the supplier quantity is greater than entered from user, set minimal.
                    if qty:
                        res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                    qty = min_qty
        dt = self._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        qty = qty or 1.0
        res['value'].update({'date_planned': date_planned or dt})
        if qty:
            res['value'].update({'product_qty': qty})

        price = price_unit
        if price_unit is False or price_unit is None:
            # - determine price_unit and taxes_id
            if pricelist_id:
                date_order_str = datetime.strptime(date_order, DEFAULT_SERVER_DATETIME_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
                price = product.product_tmpl_id.seller_ids.cbpo_after_unit_price
            else:
                price = product.product_tmpl_id.seller_ids.cbpo_after_unit_price

        taxes = account_tax.browse(cr, uid, map(lambda x: x.id, product.supplier_taxes_id))
        fpos = fiscal_position_id and account_fiscal_position.browse(cr, uid, fiscal_position_id, context=context) or False
        taxes_ids = account_fiscal_position.map_tax(cr, uid, fpos, taxes)
        price = self.pool['account.tax']._fix_tax_included_price(cr, uid, price, product.supplier_taxes_id, taxes_ids)
        res['value'].update({'price_unit': price, 'taxes_id': taxes_ids})

        return res

    def get_domain_category_id(self, cr, uid, ids, cbpo_line_category, context=None):
        mach = []
        lids = self.pool.get('product.product').search(cr, uid, [
            ('categ_id.id', '=', cbpo_line_category)])
        print lids
        return {'domain': {'product_id': [('id', '=', lids)]}}

class cbpo_delivery_term(models.Model):
    _name = 'cbpo.delivery.term'

    name = fields.Char(string="name")