# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _


class calc_currency(models.Model):
    _inherit = 'stock.landed.cost.lines'

    @api.one
    def _cbpo_price_unit(self):
        self.cbpo_price_unit = self.price_unit

    cbpo_amount_currency = fields.Float(string="Amount of Currency", digits=(16, 2),
                                        help='Payment amount in the partner currency')
    cbpo_currency_id = fields.Many2one('res.currency', string="Currency",
                                       help="Select secondary currency.")
    cbpo_price_unit = fields.Float(compute='_cbpo_price_unit', string="Cost", digits=(16, 2),)

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
                raise exceptions.ValidationError('Please Select Currency!')
        result['value'] = {
            'price_unit': price_unit,
        }
        return result



class calc_currency(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    @api.one
    def _cbpo_total_cost(self):
        self.cbpo_total_cost = self.former_cost + self.additional_landed_cost

    cbpo_total_cost = fields.Float(compute='_cbpo_total_cost', string="Total Cost", digits=(16, 2),)


class cbpo_landed_cost(models.Model):
    _inherit = 'stock.landed.cost'

    @api.one
    def _cbpo_land_costs(self):
        if len(self.valuation_adjustment_lines) > 0:
            for cost in self.valuation_adjustment_lines:
                self.cbpo_land_costs += cost.additional_landed_cost

    @api.one
    def _cbpo_products_costs(self):
        if len(self.valuation_adjustment_lines) > 0:
            for cost in self.valuation_adjustment_lines:
                self.cbpo_products_costs += cost.former_cost

    @api.one
    def _cbpo_all_total(self):
        self.cbpo_all_total = self.cbpo_land_costs + self.cbpo_products_costs

    cbpo_land_costs = fields.Float(compute='_cbpo_land_costs', string="Land Costs")
    cbpo_products_costs = fields.Float(compute='_cbpo_products_costs', string="Products Costs")
    cbpo_all_total = fields.Float(compute='_cbpo_all_total', string="All Costs")

    def button_dummy(self, cr, uid, ids, context=None):
        return True


class change_currency_rate(models.Model):
    _inherit = 'account.move.line'

    def onchange_amount_currency(self, cr, uid, ids, amount_currency, currency_id, date=False, journal=False,
                                 context=None):
        if context is None:
            context = {}
        currency_obj = self.pool.get('res.currency')
        result = {}
        rate_id = currency_obj.search(cr, uid, [('id', '=', currency_id)], context=context)
        rcr = currency_obj.browse(cr, uid, rate_id, context=context)
        debit = 0.0
        credit = 0.0
        if (amount_currency > 0):
            if rcr.rate_silent != False:
                debit = amount_currency / rcr.rate_silent
            else:
                raise exceptions.ValidationError('Please Select Currency!')
        elif (amount_currency < 0):
            if rcr.rate != False:
                credit = - (amount_currency / rcr.rate)
            else:
                raise exceptions.ValidationError('Please Select Currency!')
        result['value'] = {
            'debit': debit,
            'credit': credit
        }
        return result
