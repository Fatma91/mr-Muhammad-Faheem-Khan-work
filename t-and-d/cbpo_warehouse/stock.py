# -*- coding: utf-8 -*-
#
#
#    Author: Alexandre Fayolle
#    Copyright 2013 Camptocamp SA
#
#    Author: Damien Crier
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp import models, api, fields


class StockMove(models.Model):
    _inherit = 'stock.move'
    _order = 'date_expected desc, sequence, id'

    @api.one
    def _cbpo_client_code(self):
        sale_order = self.env['sale.order']
        purchase_order = self.env['purchase.order']
        sale_line = self.env['sale.order.line']
        purchase_line = self.env['purchase.order.line']
        name = self.picking_id.origin
        if name:
            if name[:2] == 'SO':
                order = sale_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    res = sale_order.browse(order[0].id)
                    self.cbpo_client_code = res.partner_id.ref
            elif name[:2] == 'PO':
                order = purchase_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    res1 = purchase_order.browse(order[0].id)
                    sale = sale_order.search([('name', '=', res1.origin)])
                    if len(sale) > 0:
                        res2 = sale_order.browse(sale[0].id)
                        self.cbpo_client_name = res2.partner_id.name
        else:
            pass
        return True

    @api.one
    def _cbpo_client_name(self):
        sale_order = self.env['sale.order']
        purchase_order = self.env['purchase.order']
        name = self.picking_id.origin
        if name:
            if name[:2] == 'SO':
                order = sale_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    res = sale_order.browse(order[0].id)
                    self.cbpo_client_name = res.partner_id.name
            elif name[:2] == 'PO':
                order = purchase_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    res1 = purchase_order.browse(order[0].id)
                    sale = sale_order.search([('name', '=', res1.origin)])
                    if len(sale) > 0:
                        res2 = sale_order.browse(sale[0].id)
                        self.cbpo_client_name = res2.partner_id.name
        else:
            pass

    @api.one
    def _cbpo_floor(self):
        sale_order = self.env['sale.order']
        purchase_order = self.env['purchase.order']
        sale_line = self.env['sale.order.line']
        purchase_line = self.env['purchase.order.line']
        name = self.picking_id.origin
        if name:
            if name[:2] == 'SO':
                order = sale_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    line = sale_line.search([('order_id', '=', order[0].id)])[0].id
                    res = sale_line.browse(line)
                    self.cbpo_floor = res.cbpo_floor
            elif name[:2] == 'PO':
                order = purchase_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    line = purchase_line.search([('order_id', '=', order[0].id)])[0].id
                    res = purchase_line.browse(line)
                    self.cbpo_floor = res.cbpo_floor
        else:
            pass

    @api.one
    def _cbpo_area(self):
        sale_order = self.env['sale.order']
        purchase_order = self.env['purchase.order']
        sale_line = self.env['sale.order.line']
        purchase_line = self.env['purchase.order.line']
        name = self.picking_id.origin
        if name:
            if name[:2] == 'SO':
                order = sale_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    line = sale_line.search([('order_id', '=', order[0].id)])[0].id
                    res = sale_line.browse(line)
                    self.cbpo_area = res.cbpo_area
            elif name[:2] == 'PO':
                order = purchase_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    line = purchase_line.search([('order_id', '=', order[0].id)])[0].id
                    res = purchase_line.browse(line)
                    self.cbpo_area = res.cbpo_area
        else:
            pass

    @api.one
    def _cbpo_finishes(self):
        sale_order = self.env['sale.order']
        purchase_order = self.env['purchase.order']
        sale_line = self.env['sale.order.line']
        purchase_line = self.env['purchase.order.line']
        name = self.picking_id.origin
        if name:
            if name[:2] == 'SO':
                order = sale_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    line = sale_line.search([('order_id', '=', order[0].id)])[0].id
                    res = sale_line.browse(line)
                    self.cbpo_finishes = res.cbpo_finishes.name
            elif name[:2] == 'PO':
                order = purchase_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    line = purchase_line.search([('order_id', '=', order[0].id)])[0].id
                    res = purchase_line.browse(line)
                    self.cbpo_finishes = res.cbpo_finishes.name
        else:
            pass

    @api.one
    def _cbpo_currency(self):
        sale_order = self.env['sale.order']
        purchase_order = self.env['purchase.order']
        sale_line = self.env['sale.order.line']
        purchase_line = self.env['purchase.order.line']
        name = self.picking_id.origin
        if name:
            if name[:2] == 'SO':
                order = sale_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    line = sale_line.search([('order_id', '=', order[0].id)])[0].id
                    res = sale_line.browse(line)
                    self.cbpo_currency = res.order_id.pricelist_id.currency_id.id
            elif name[:2] == 'PO':
                order = purchase_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    line = purchase_line.search([('order_id', '=', order[0].id)])[0].id
                    res = purchase_line.browse(line)
                    self.cbpo_currency = res.order_id.currency_id.id
        else:
            pass

    @api.one
    def _sale_oder(self):
        sale_order = self.env['sale.order']
        purchase_order = self.env['purchase.order']
        sale_line = self.env['sale.order.line']
        purchase_line = self.env['purchase.order.line']
        name = self.picking_id.origin
        if name:
            if name[:2] == 'SO':
                self.cbpo_sale_order = self.picking_id.origin
            elif name[:2] == 'PO':
                order = purchase_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    res = purchase_order.browse(order[0].id)
                    self.cbpo_sale_order = res.origin
        else:
            pass

    @api.one
    def _cbpo_performa(self):
        sale_order = self.env['sale.order']
        purchase_order = self.env['purchase.order']
        sale_line = self.env['sale.order.line']
        purchase_line = self.env['purchase.order.line']
        name = self.picking_id.origin
        if name:
            if name[:2] == 'SO':
                order = purchase_order.search([('origin', '=', self.picking_id.origin)])
                if len(order) > 0:
                    res = purchase_order.browse(order[0].id)
                    self.cbpo_performa = res.cbpo_proforma_invoice_no
            elif name[:2] == 'PO':
                order = purchase_order.search([('name', '=', self.picking_id.origin)])
                if len(order) > 0:
                    res = purchase_order.browse(order[0].id)
                    self.cbpo_performa = res.cbpo_proforma_invoice_no
        else:
            pass


    sequence = fields.Integer()
    cbpo_client_code = fields.Char(string="Client code", compute='_cbpo_client_code')
    cbpo_client_name = fields.Char(string="Customer Name", compute='_cbpo_client_name')
    cbpo_floor = fields.Char(string="Floor", compute='_cbpo_floor')
    cbpo_area = fields.Char(string="Area", compute='_cbpo_area')
    item_name = fields.Char(related='product_id.item_name_id.name', string="Item Name")
    cbpo_supplier_item_code = fields.Char(string="Supplier Item Code",related='product_id.product_tmpl_id.seller_ids.product_code')
    cbpo_supplier_name = fields.Many2one('res.partner', string="Supplier Name", related='product_id.product_tmpl_id.seller_ids.name')
    cbpo_finishes = fields.Char(string="Finishes", compute='_cbpo_finishes')
    cbpo_sale_order = fields.Char(string="SO.#", compute='_sale_oder')
    cbpo_pieces = fields.Integer(string="Pieces", default=False)
    cbpo_currency = fields.Many2one('res.currency', string="Currency", compute='_cbpo_currency')
    cbpo_performa = fields.Char(string="Performa.#", compute='_cbpo_performa')

    # @api.model
    # def _get_invoice_line_vals(self, move, partner, inv_type):
    #     res = super(StockMove, self)._get_invoice_line_vals(move,
    #                                                         partner,
    #                                                         inv_type)
    #     res['sequence'] = move.sequence
    #     return res


# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
#
#     # @api.depends('move_lines')
#     # def _get_max_line_sequence(self):
#     #     for picking in self:
#     #         picking.max_line_sequence = (
#     #             max(picking.mapped('move_lines.sequence')) + 10
#     #         )
#
#     max_line_sequence = fields.Integer(string='Max sequence in lines',
#                                        compute='_get_max_line_sequence')
