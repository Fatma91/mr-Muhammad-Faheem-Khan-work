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

from openerp import models, api


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.model
    def _run_move_create(self, procurement):
        res = super(ProcurementOrder, self)._run_move_create(procurement)
        if procurement.sale_line_id.sequence:
            res.update({'sequence': procurement.sale_line_id.sequence,})
            res.update({'sequence': procurement.sale_line_id.sequence,})

        return res



# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     @api.model
#     def _prepare_order_line_procurement(self, order, line, group_id=False):
#         res = super(SaleOrder, self)._prepare_order_line_procurement(order, line, group_id=False)
#         res.update({'cbpo_floor': line.cbpo_floor,
#                     'cbpo_area': line.cbpo_area,
#                     'item_name': line.item_name.id,
#                     'cbpo_partner_id': order.partner_id.id,
#                     'cbpo_client_code': line.cbpo_client_code,
#                     'cbpo_finishes': line.cbpo_finishes,
#                     })



# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
#
#     @api.model
#     def _prepare_order_line_move(self, order, order_line, picking_id, group_id):
#         res = super(PurchaseOrder, self)._prepare_order_line_move(order, order_line, picking_id, group_id)
#         res.update({'cbpo_floor': order_line.cbpo_floor,
#                     'cbpo_area': order_line.cbpo_area,
#                     'item_name': order_line.item_name.id,
#                     'cbpo_supplier': order_line.cbpo_supplier,
#                     'cbpo_supplier_item_code': order_line.cbpo_supplier_item_code,
#                     'cbpo_finishes': order_line.cbpo_finishes,
#                     })
#
#         return res