# -*- coding: utf-8 -*-

from openerp.osv import osv, fields, expression
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp


class cbpo_product(osv.osv):
    _inherit = 'pricelist.partnerinfo'

    _columns = {
        'price_first': fields.float('Unit Price'),
        'disacount': fields.float('Disacount %'),
        'production_time': fields.date('Production Time'),
        'shipping_time': fields.date('Shipping Time'),
        'duty_clearance': fields.date('Duty clearance'),
    }

    def onchange_all(self, cr, uid, ids, price_first, disacount, context=None):
        """
        onchange handler of qty.
        Set total
        """
        if context is None:
            context = {}
        contractor_total = price_first * (1 - (disacount or 0.0) / 100.0)

        val = {
            'price': contractor_total,

        }
        return {'value': val}


cbpo_product()


class cbpo_product_supplierinfo(osv.osv):
    _inherit = 'product.supplierinfo'

    # def _after_discount(self, cr, uid, ids, name, arg, context=None):
    #     res = {}
    #     for obj in self.browse(cr, uid, ids, context=context):
    #         res[obj.id] = obj.cbpo_unit_price - (obj.cbpo_unit_price * (obj.cbpo_discount or 0.0) / 100.0)
    #     return res

    _columns = {
        'cbpo_supplier_type': fields.selection([('standard', 'Standard'), ('non_standard', 'Non Standard')],
                                               'Supplier Lead Time Type', ),
        'cbpo_production_time': fields.integer('Production Time'),
        'cbpo_shipping_time': fields.integer('Shipping Time'),
        'cbpo_duty_clearance': fields.integer('Duty clearance'),

        'cbpo_production_time_non': fields.integer('Production Time'),
        'cbpo_shipping_time_non': fields.integer('Shipping Time'),
        'cbpo_duty_clearance_non': fields.integer('Duty clearance'),
        'delay_stand': fields.integer('Delivery Lead Time', ),
        'delay_non': fields.integer('Delivery Lead Time', ),

        'cbpo_unit_price': fields.float('Unit Price'),
        'cbpo_discount': fields.float('Discount'),
        'cbpo_after_unit_price': fields.float('After Unit Price'),
        'installation_time': fields.float('Installation Time'),
    }

    _defaults = {
        'cbpo_supplier_type': 'standard',
    }

    def onchange_after_discount(self, cr, uid, ids, cbpo_unit_price, cbpo_discount,  context=None):
        if context is None:
            context = {}
        after_discount = cbpo_unit_price - (cbpo_unit_price * (cbpo_discount or 0.0) / 100.0)
        val = {
            'cbpo_after_unit_price': after_discount,
        }

        return {'value': val}

    def onchange_supplier_name(self, cr, uid, ids, supplier_name_id, context=None):
        if context is None:
            context = {}
        supplier_model = self.pool.get('res.partner').browse(cr, uid, supplier_name_id, context=context)
        val = {
            'cbpo_production_time': supplier_model.cbpo_production_time_stand,
            'cbpo_shipping_time': supplier_model.cbpo_shipping_time_stand,
            'cbpo_duty_clearance': supplier_model.cbpo_clearance_stand,

            'cbpo_production_time_non': supplier_model.cbpo_production_time_non_stand,
            'cbpo_shipping_time_non': supplier_model.cbpo_shipping_time_non_stand,
            'cbpo_duty_clearance_non': supplier_model.cbpo_clearance_non_stand,

            'cbpo_discount': supplier_model.cbpo_supplier_discount,
        }

        return {'value': val}

    def onchange_time_amount(self, cr, uid, ids, production_time, shipping_time, duty_clearance, production_time_,
                             shipping_time_, duty_clearance_, date=False,
                             journal=False,
                             context=None):
        if context is None:
            context = {}
        result = {}
        sum = production_time + shipping_time + duty_clearance
        sum_non = production_time_ + shipping_time_ + duty_clearance_
        result['value'] = {
            'delay_stand': sum,
            'delay_non': sum_non,
        }
        return result


cbpo_product_supplierinfo()


class new_module(osv.osv):
    _name = 'new_module.new_module'
    _description = 'New Description'

    _columns = {
        'name': fields.char(),
    }


new_module()


class item_name(osv.osv):
    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            categories = name.split(' / ')
            parents = list(categories)
            child = parents.pop()
            domain = [('name', operator, child)]
            if parents:
                names_ids = self.name_search(cr, uid, ' / '.join(parents), args=args, operator='ilike', context=context,
                                             limit=limit)
                category_ids = [name_id[0] for name_id in names_ids]
                if operator in expression.NEGATIVE_TERM_OPERATORS:
                    category_ids = self.search(cr, uid, [('id', 'not in', category_ids)])
                    domain = expression.OR([[('parent_id', 'in', category_ids)], domain])
                else:
                    domain = expression.AND([[('parent_id', 'in', category_ids)], domain])
                for i in range(1, len(categories)):
                    domain = [[('name', operator, ' / '.join(categories[-1 - i:]))], domain]
                    if operator in expression.NEGATIVE_TERM_OPERATORS:
                        domain = expression.AND(domain)
                    else:
                        domain = expression.OR(domain)
            ids = self.search(cr, uid, expression.AND([domain, args]), limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _name = "item.name"

    _description = "Item Name"
    _columns = {
        'name': fields.char('Name', required=True, translate=True, select=True),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Name'),
        'parent_id': fields.many2one('item.name', 'Parent Category', select=True, ondelete='cascade'),
        'child_id': fields.one2many('product.category', 'parent_id', string='Child Categories'),
        'sequence': fields.integer('Sequence', select=True,
                                   help="Gives the sequence order when displaying a list of product categories."),
        'type': fields.selection([('view', 'View'), ('normal', 'Normal')], 'Category Type',
                                 help="A category of the view type is a virtual category that can be used as the parent of another category to create a hierarchical structure."),
        'parent_left': fields.integer('Left Parent', select=1),
        'parent_right': fields.integer('Right Parent', select=1),
    }

    _defaults = {
        'type': 'normal',
    }

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    _constraints = [
        (osv.osv._check_recursion, 'Error ! You cannot create recursive categories.', ['parent_id'])
    ]


class cbpo_product_template(osv.osv):
    _inherit = 'product.template'

    def _product_available(self, cr, uid, ids, name, arg, context=None):
        res = {}
        supplierinfo = self.pool.get('product.supplierinfo')
        for obj in self.browse(cr, uid, ids, context=context):
            eq = supplierinfo.search(cr, uid, [('product_tmpl_id', '=', obj.id)], context=context)
            if eq:
                info_brows = supplierinfo.browse(cr, uid, eq, context=context)
                if info_brows.cbpo_supplier_type == "standard":
                    res[obj.id] = obj.installation_time + float(info_brows.delay_stand)
                elif info_brows.cbpo_supplier_type == "non_standard":
                    res[obj.id] = obj.installation_time + float(info_brows.delay_non)
        return res

    _columns = {
        'cbpo_amount_currency': fields.float(string="Amount of Currency", digits=(16, 2),
                                             help='Payment amount in the partner currency'),
        'cbpo_currency_id': fields.many2one('res.currency', string="Currency",
                                            help="Select secondary currency."),
        'product_attribute_line': fields.one2many('cbpo.product.attribute', 'pro_temp_id', 'CPAI'),
        'lst_price': fields.float(string='Public Price', digits_compute=dp.get_precision('Product Price')),
        'installation_time': fields.float('Installation Time'),
        'sale_delay': fields.function(_product_available, type='float', string='Customer Lead Time',
                                      help="The average delay in days between the confirmation of the customer order and the delivery of the finished products. It's the time you promise to your customers."),
        # 'cbpo_product_type': fields.many2one('product.category', 'Product Type'),
    }

    def _check_supplier(self, cr, uid, ids, context=None):
        self_obj = self.browse(cr, uid, ids, context=context);
        lenth = len(self_obj.seller_ids)
        if lenth <= 1:
            return True
        return False

    _constraints = [(_check_supplier, 'Error: Please enter One supplier', ['seller_ids']), ]

    def onchange_amount_currency(self, cr, uid, ids, cbpo_amount_currency, cbpo_currency_id, date=False, journal=False,
                                 context=None):
        if context is None:
            context = {}
        currency_obj = self.pool.get('res.currency')
        result = {}
        rate_id = currency_obj.search(cr, uid, [('id', '=', cbpo_currency_id)], context=context)
        rcr = currency_obj.browse(cr, uid, rate_id, context=context)
        price_unit = 0.0
        if cbpo_amount_currency:
            if rcr.rate_silent != False:
                price_unit = cbpo_amount_currency / rcr.rate_silent
            else:
                raise osv.except_osv(_('Warning!'), _('Please Select Currency!'))

        result['value'] = {
            'list_price': price_unit,
        }
        return result


class cbpo_product_template(osv.osv):
    _inherit = 'product.product'

    _columns = {
        'product_type_id': fields.many2one('product.category', 'Product Type'),
        'item_name_id': fields.many2one('item.name', 'Product Type'),
        'cbpo_product_type': fields.many2one('product.category', 'Product Type'),

        'cbpo_amount_currency': fields.float(string="Standard public price", digits=(16, 2),
                                             help='Payment amount in the partner currency'),
        'cbpo_currency_id': fields.many2one('res.currency', string="Currency",
                                            help="Select secondary currency."),
    }

    def onchange_amount_currency(self, cr, uid, ids, cbpo_amount_currency, cbpo_currency_id, date=False, journal=False,
                                 context=None):
        if context is None:
            context = {}
        currency_obj = self.pool.get('res.currency')
        result = {}
        rate_id = currency_obj.search(cr, uid, [('id', '=', cbpo_currency_id)], context=context)
        rcr = currency_obj.browse(cr, uid, rate_id, context=context)
        price_unit = 0.0
        if cbpo_amount_currency:
            if rcr.rate_silent != False:
                price_unit = cbpo_amount_currency / rcr.rate_silent
            else:
                raise osv.except_osv(_('Warning!'), _('Please Select Currency!'))

        result['value'] = {
            'price_unit': price_unit,
        }
        return result


class cbpo_catogry_code(osv.osv):
    _name = 'cbpo.catogry.code'

    _columns = {

        'name': fields.char(string="Code")

    }


class cbpo_product_category(osv.osv):
    _inherit = 'product.category'

    _columns = {

        'cbpo_code_id': fields.many2one('cbpo.catogry.code', string="Serial Code"),
    }


class cbpo_product_attribute(osv.osv):
    _name = 'cbpo.product.attribute'

    def _get_my_name(self, cr, uid, ids, field_name, args, context=None):
        res = dict.fromkeys(ids, '')
        for obj in self.browse(cr, uid, ids, context=context):
            product_product = self.pool.get('product.product')
            rec = product_product.search(cr, uid, [('product_tmpl_id', '=', obj.pro_temp_id.id)], context=context)
            val = product_product.browse(cr, uid, rec)
            res[obj.id] = val.id

        return res

    _columns = {
        'pro_temp_id': fields.many2one('product.template', 'Product Name', select=True, ondelete='cascade'),
        'product_product_id': fields.function(_get_my_name, string='PIN', type='float', store=True),
        'product_attribute_id': fields.many2one('product.attribute', 'Finishes'),
        'name': fields.related('product_attribute_id', 'name', type='char', string='Name', store=True, ),
    }

# def onchange_attribute_name(self, cr, uid, ids, product_attribute_id, context=None):
#     if context is None:
#         context = {}
#     product_attribute = self.pool.get('product.attribute').browse(cr, uid, product_attribute_id, context=context)
#     val = {
#         'name': product_attribute.name,
#     }
#     return {'value': val}


# HAZEM 8/11
