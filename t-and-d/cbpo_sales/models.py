# -*- coding: utf-8 -*-

import time
from openerp import models, fields, api
from openerp import SUPERUSER_ID
from openerp.exceptions import ValidationError
from openerp.tools.translate import _
from openerp.osv import osv
from datetime import date, timedelta
import datetime
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import re


class cbpoSales(models.Model):
    _inherit = ['sale.order']

    @api.one
    @api.constrains('order_line')
    def _check_order_lines_sequence(self):
        """
        check that the sequence is unique per purchase order line.
        """
        all_sequences = self.order_line.mapped('sequence')
        sequences = list(set(all_sequences))
        if len(all_sequences) != len(sequences):
            raise ValidationError(
                _('The sequence must be unique per sale order!') + ".\n" +
                _('The next sequence numbers are already used') + ":\n" +
                str(sequences))

    def old_method(self, cr, uid, ids, context=None):
        return ids

    @api.depends('date_order', 'cbpo_type')
    @api.one
    def _client_order_ref(self):
        cus = self.env['res.partner']
        use = self.env['res.users']
        pro = self.env['project.project']
        # sales = self.env['sale.order']
        # ids = self.ids
        # salesearch = sales.search([('id', '=', ids)])
        # sale_rec = sales.browse(salesearch)
        prosearch = pro.search([('partner_id', '=', self.partner_id.id)])
        cus_rec = cus.browse(self.partner_id.id)
        use_rec = use.browse(self.user_id.id)
        # timer = self.date_order.datetime.strftime('%Y-%m-%d')\
        my_time = self.date_order
        aray_time = my_time.split(' ')
        timer = aray_time[0]
        name_sale = self.name
        self.cbpo_client_order_ref = str(timer) +"-"+ str(self.cbpo_type.cbpo_code_id.name) + name_sale +"-"+ str(
                cus_rec.sale_order_count) + str(cus_rec.ref) +"-"+ str(len(prosearch)) + str(use_rec.cbpo_user_code)
        return True


    @api.one
    def _expected_delivery_date(self):
        sale_order_line_obj = self.env['sale.order.line']
        delay = []
        if len(self.order_line.ids)> 0:
            for line in self.order_line.ids:
                for line1 in sale_order_line_obj.browse(line):
                    delay.append(line1.delay)
            days = int(max(delay))
            self.cbpo_expected_delivery_date = date.today() + relativedelta(days=days)

# fatma update here
#     def _get_expected_weeks(self):
#         sale_obj = self.env['sale.order.line']
#         delay = []
#         if len(self.order_line.ids) > 0:
#             for line in self.order_line.ids:
#                 for line1 in sale_obj.browse(line):
#                     delay.append(line1.delay)
#             days = int(max(delay))
#             self.cbpo_expected_delivery_weeks = relativedelta(days=days)


    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True,
                                 change_default=True, select=True, track_visibility='always')
    cbpo_type_id = fields.Many2one('cbpo.type', string="Type")
    cbpo_attention_to = fields.Many2one('res.partner', string="Attention to", domain=[('customer', '=', True)])
    cbpo_date_of_advance = fields.Date(string="Date of advance payment")
    cbpo_date_of_finishes = fields.Date(string="Date of finishes / Selection")
    cbpo_final_Layout_date = fields.Date(string="Final Layout date")
    cbpo_expected_delivery_date = fields.Datetime(compute='_expected_delivery_date',string="Expected delivery date", readonly=False)
    cbpo_client_order_ref = fields.Char(compute='_client_order_ref', string="Offer REF.", store=True)
    # cbpo_mktime = fields.Char(string="MKTime",default=_compute_mktime)
    cbpo_type = fields.Many2one('product.category',string="Product Range",domain=[('parent_id', '=', False)])
    state = fields.Selection(selection=[('draft', 'Draft Quotation'),
                                        ('sent', 'Quotation Sent'),
                                        ('revised', 'Reviseded'),
                                        ('cancel', 'Cancelled'),
                                        ('waiting_date', 'Waiting Schedule'),
                                        ('progress', 'Sales Order'),
                                        ('manual', 'Sale to Invoice'),
                                        ('shipping_except', 'Shipping Exception'),
                                        ('invoice_except', 'Invoice Exception'),
                                        ('done', 'Done')], string="Status", readonly=True, copy=False, help="Gives the status of the quotation or sales order.\
                                                      \nThe exception status is automatically set when a cancel operation occurs \
                                                      in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
                                                       but waiting for the scheduler to run on the order date.",
                             select=True)
    cbpo_subject = fields.Many2one('cbpo.subject', string="Subject" ,required = True)

    #fatma updated here
    cbpo_contract_delivery_date = fields.Date(string="contract delivery date")
    cbpo_guarantee = fields.Text(string="Guarantee")
    cbpo_offer_validtiy = fields.Selection([('one', 'One week'),
                                            ('two', '2 week'), ('four', '4 week'), ('month', 'One month')],
                                           required=True)
    cbpo_attachment= fields.Selection([('done', 'Done'),
                                            ('not applicable', 'Not Applicable')],
                                           required=True)
    # cbpo_expected_delivery_weeks = fields.Date(compute='_get_expected_weeks',string="Expected Delivery(weeks)")
    #fatma end update

    def revised_cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        sale_order_line_obj = self.pool.get('sale.order.line')
        account_invoice_obj = self.pool.get('account.invoice')
        for sale in self.browse(cr, uid, ids, context=context):
            for inv in sale.invoice_ids:
                if inv.state not in ('draft', 'cancel'):
                    raise osv.except_osv(
                        _('Cannot cancel this sales order!'),
                        _('First cancel all invoices attached to this sales order.'))
                inv.signal_workflow('invoice_cancel')
            line_ids = [l.id for l in sale.order_line if l.state != 'revised']
            sale_order_line_obj.my_button_cancel(cr, uid, line_ids, context=context)
        self.write(cr, uid, ids, {'state': 'revised'})
        return True


class cbpoSalesLine(models.Model):
    _inherit = ['sale.order.line']
    _order = "sequence"

    @api.one
    def _discount_price(self):
        price = self.price_unit - (self.price_unit * (self.discount or 0.0) / 100.0)
        self.cbpo_discount_price = price

    @api.one
    def _price_before_discount(self):
        tex = self.price_unit * self.product_uom_qty
        self.cbpo_total_price = tex

    @api.one
    def _price_after_discount(self):
        tex = self.price_unit - (self.price_unit * self.discount / 100)
        self.cbpo_price_after_disc = tex

    @api.one
    def _cbpo_client_code(self):
        self.cbpo_client_code = self.order_id.partner_id.ref

    # @api.one
    # def _cbpo_product_category(self):
    #     self.cbpo_product_category = self.order_id.cbpo_product_category

    # index = fields.Integer(compute='_compute_index', string="Sequence")
    sequence = fields.Integer(
        string='Seq.',
        help="Gives the sequence of this line when displaying the"
             " sales order.")

    # cbpo_product_category = fields.Many2one(related='order_id.cbpo_product_category',comodel_name='product.category',string="Product Test")
    cbpo_product_category = fields.Many2one('product.category',string="Product Category")
    cbpo_line_category = fields.Many2one(comodel_name='product.category',string="Product Type",)
    item_name = fields.Many2one(comodel_name='item.name', string="Product Type")
    product_id = fields.Many2one('product.product', 'Model Name/code', change_default=True, domain=[('sale_ok', '=', True)],
                                 readonly=True, states={'draft': [('readonly', False)]}, ondelete='restrict')
    cbpo_client_code = fields.Char(compute='_cbpo_client_code',string="Client code")
    cbpo_floor = fields.Char(string="Floor")
    cbpo_area = fields.Char(string="Area")
    # cbpo_tmpl_id = fields.Many2one(compute='_tmpl_id','product.template', string="tmpl" )
    cbpo_supplier = fields.Char(related='product_id.product_tmpl_id.seller_ids.name.name', string="Supplier",
                                domain=[('supplier', '=', True)])
    cbpo_supplier_item_code = fields.Char(related='product_id.product_tmpl_id.seller_ids.product_code',
                                          string="Supplier Item Code", )
    # cbpo_cost_price = fields.Float()
    cbpo_finishes = fields.Many2one('cbpo.product.attribute', string="Finishes", )
    cbpo_discount_price = fields.Float(compute='_discount_price', string='Price after Discount')
    cbpo_total_price = fields.Float(compute='_price_before_discount', string='Total before Discount')
    cbpo_price_after_disc = fields.Float(compute='_price_after_discount', string='Total before Discount')
    cbpo_unit_price1 = fields.Float(string="My Unit Price")
    cbpo_comments = fields.Text(string="Comments")
    state = fields.Selection(
        selection=[('cancel', 'Cancelled'), ('revised', 'Reviseded'), ('draft', 'Draft'), ('confirmed', 'Confirmed'),
                   ('exception', 'Exception'), ('done', 'Done')],
        string='Status', required=True, readonly=True, copy=False,
        help='* The \'Draft\' status is set when the related sales order in draft status. \
                    \n* The \'Confirmed\' status is set when the related sales order is confirmed. \
                    \n* The \'Exception\' status is set when the related sales order is set as exception. \
                    \n* The \'Done\' status is set when the sales order line has been picked. \
                    \n* The \'Cancelled\' status is set when a user cancel the sales order related.\
                    \n* The \'Reviseded\' status is set when a user revised the sales order related.')

    def get_domain_category_id(self, cr, uid, ids, cbpo_line_category, context=None):
        mach = []
        lids = self.pool.get('product.product').search(cr, uid, [
            ('categ_id.id', '=', cbpo_line_category)])
        print lids
        return {'domain': {'product_id': [('id', '=', lids)]}}

    @api.model
    def default_get(self, fields_list):
        """
        Overwrite the default value of the sequence field taking into account
        the current number of lines in the purchase order. If is not call from
        the purchase order will use the default value.
        """
        res = super(cbpoSalesLine, self).default_get(fields_list)
        res.update({'sequence': len(self._context.get('order_line', [])) + 1})
        return res

    def my_button_cancel(self, cr, uid, ids, context=None):
        lines = self.browse(cr, uid, ids, context=context)
        for line in lines:
            if line.invoiced:
                raise osv.except_osv(_('Invalid Action!'),
                                     _('You cannot cancel a sales order line that has already been invoiced.'))
        procurement_obj = self.pool['procurement.order']
        procurement_obj.cancel(cr, uid, sum([l.procurement_ids.ids for l in lines], []), context=context)
        return self.write(cr, uid, ids, {'state': 'revised'})

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                          lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False,
                          flag=False, context=None):
        context = context or {}
        lang = lang or context.get('lang', False)
        if not partner_id:
            raise osv.except_osv(_('No Customer Defined!'),
                                 _('Before choosing a product,\n select a customer in the sales form.'))
        warning = False
        product_uom_obj = self.pool.get('product.uom')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        partner = partner_obj.browse(cr, uid, partner_id)
        lang = partner.lang
        context_partner = context.copy()
        context_partner.update({'lang': lang, 'partner_id': partner_id})

        if not product:
            return {'value': {'th_weight': 0,
                              'product_uos_qty': qty}, 'domain': {'product_uom': [],
                                                                  'product_uos': []}}
        if not date_order:
            date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        result = {}
        warning_msgs = ''
        product_obj = product_obj.browse(cr, uid, product, context=context_partner)

        uom2 = False
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom)
            if product_obj.uom_id.category_id.id != uom2.category_id.id:
                uom = False
        if uos:
            if product_obj.uos_id:
                uos2 = product_uom_obj.browse(cr, uid, uos)
                if product_obj.uos_id.category_id.id != uos2.category_id.id:
                    uos = False
            else:
                uos = False

        fpos = False
        if not fiscal_position:
            fpos = partner.property_account_position or False
        else:
            fpos = self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position)
        if update_tax:  # The quantity only have changed
            # The superuser is used by website_sale in order to create a sale order. We need to make
            # sure we only select the taxes related to the company of the partner. This should only
            # apply if the partner is linked to a company.
            if uid == SUPERUSER_ID and partner.company_id:
                taxes = product_obj.taxes_id.filtered(lambda r: r.company_id == partner.company_id)
            else:
                taxes = product_obj.taxes_id
            result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, taxes)

        if not flag:
            result['name'] = \
                self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
            if product_obj.description_sale:
                result['name'] += '\n' + product_obj.description_sale
        domain = {}
        if (not uom) and (not uos):
            result['product_uom'] = product_obj.uom_id.id
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
                uos_category_id = product_obj.uos_id.category_id.id
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
                uos_category_id = False
            result['th_weight'] = qty * product_obj.weight
            domain = {'product_uom':
                          [('category_id', '=', product_obj.uom_id.category_id.id)],
                      'product_uos':
                          [('category_id', '=', uos_category_id)]}
        elif uos and not uom:  # only happens if uom is False
            result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
            result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
            result['th_weight'] = result['product_uom_qty'] * product_obj.weight
        elif uom:  # whether uos is set or not
            default_uom = product_obj.uom_id and product_obj.uom_id.id
            q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
            result['th_weight'] = q * product_obj.weight  # Round the quantity up
        # cbpo_price = product_obj.standard_price
        # result['cbpo_cost_price'] = cbpo_price
        if not uom2:
            uom2 = product_obj.uom_id
        # get unit price

        if not pricelist:
            warn_msg = _('You have to select a pricelist or a customer in the sales form !\n'
                         'Please set one before choosing a product.')
            warning_msgs += _("No Pricelist ! : ") + warn_msg + "\n\n"
        else:
            ctx = dict(
                context,
                uom=uom or result.get('product_uom'),
                date=date_order,
            )
            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                                                                 product, qty or 1.0, partner_id, ctx)[pricelist]
            if price is False:
                warn_msg = _("Cannot find a pricelist line matching this product and quantity.\n"
                             "You have to change either the product, the quantity or the pricelist.")

                warning_msgs += _("No valid pricelist line found ! :") + warn_msg + "\n\n"
            else:
                result.update({'price_unit': price})
                result.update({'cbpo_unit_price1': price})
                if context.get('uom_qty_change', False):
                    return {'value': {'price_unit': price}, 'domain': {}, 'warning': False}
        if warning_msgs:
            warning = {
                'title': _('Configuration Error!'),
                'message': warning_msgs
            }
        return {'value': result, 'domain': domain, 'warning': warning}


        # @api.one
        # def _compute_index(self):
        #     model1 = self.env['product.product']
        #     model2 = self.env['product.category']
        #     temp_max = 0
        #     listnum = []
        #     res = None
        #     val1 = self.product_tmpl_id.categ_id.id
        #     record2 = model2.browse(cr, uid, val1, context=context)
        #     product_ids = model1.search(cr, uid, ['&', '&', ('cbpo_auto', '!=', 0), ('cbpo_auto', '!=', False), ('product_tmpl_id.categ_id.id', '=', val.product_tmpl_id.categ_id.id)])
        #     if(len(product_ids) > 0):
        #         if (val.cbpo_auto == 0):
        #             for record1 in  model1.browse(cr, uid, product_ids, context=context):
        #                 listnum.append(record1.cbpo_auto)
        #                 maxid = max(listnum)
        #                 temp_max = maxid + 1
        #                 res = record2.cbpo_internal_ref + '-' + str(temp_max)
        #         else:
        #             temp_max = val.cbpo_auto
        #             res = val.default_code
        #
        #     else:
        #         temp_max = 1
        #         res = record2.cbpo_internal_ref + '-' + str(temp_max)
        #
        #     self.write(cr, uid, ids, {'cbpo_auto': temp_max, 'default_code': res }, context=context)


class cbpoPartner(models.Model):
    _inherit = ['res.users']

    cbpo_user_code = fields.Char(string="User Code")


class cbpoSubject(models.Model):
    _name = 'cbpo.subject'

    name = fields.Char()
