# HAZEM works to make oppertunity to quotation >> make it WON
from openerp.osv import osv, fields
from openerp.tools.translate import _


class make_sale(osv.osv):
    _inherit = "crm.make.sale"
    _columns = {
        'current_oppertunity_id': fields.many2one('crm.lead', 'Current revision')
    }

    def makeOrder(self, cr, uid, ids, context=None):
        context = dict(context or {})
        context.pop('default_state', False)

        case_obj = self.pool.get('crm.lead')
        sale_obj = self.pool.get('sale.order')
        partner_obj = self.pool.get('res.partner')
        data = context and context.get('active_ids', []) or []
        curentId = self.read(cr, uid, ids, ['id'])
        for make in self.browse(cr, uid, ids, context=context):
            partner = make.partner_id
            partner_addr = partner_obj.address_get(cr, uid, [partner.id],
                                                   ['default', 'invoice', 'delivery', 'contact'])
            pricelist = partner.property_product_pricelist.id
            fpos = partner.property_account_position and partner.property_account_position.id or False
            payment_term = partner.property_payment_term and partner.property_payment_term.id or False
            new_ids = []
            for case in case_obj.browse(cr, uid, data, context=context):
                if not partner and case.partner_id:
                    partner = case.partner_id
                    fpos = partner.property_account_position and partner.property_account_position.id or False
                    payment_term = partner.property_payment_term and partner.property_payment_term.id or False
                    partner_addr = partner_obj.address_get(cr, uid, [partner.id],
                                                           ['default', 'invoice', 'delivery', 'contact'])
                    pricelist = partner.property_product_pricelist.id

                vals = {
                    'origin': _('Opportunity: %s') % str(case.id),
                    'section_id': case.section_id and case.section_id.id or False,
                    'categ_ids': [(6, 0, [categ_id.id for categ_id in case.categ_ids])],
                    'partner_id': partner.id,
                    'pricelist_id': pricelist,
                    'partner_invoice_id': partner_addr['invoice'],
                    'partner_shipping_id': partner_addr['delivery'],
                    'date_order': fields.datetime.now(),
                    'fiscal_position': fpos,
                    'payment_term': payment_term,
                    'note': sale_obj.get_salenote(cr, uid, [case.id], partner.id, context=context),
                    # HAZEM
                    'current_oppertunity_id': case_obj.browse(cr, uid, data, context=context).id
                }
                # results = case_obj.browse(cr, uid, data, context=context).name
                # print  results  # case_obj.browse(cr, uid,  results[0]['id'], context=context).name
                if partner.id:
                    vals['user_id'] = partner.user_id and partner.user_id.id or uid
                new_id = sale_obj.create(cr, uid, vals, context=context)
                sale_order = sale_obj.browse(cr, uid, new_id, context=context)
                case_obj.write(cr, uid, [case.id], {'ref': 'sale.order,%s' % new_id})
                new_ids.append(new_id)
                message = _("Opportunity has been <b>converted</b> to the quotation <em>%s</em>.") % (sale_order.name)
                case.message_post(body=message)
            if make.close:
                case_obj.case_mark_won(cr, uid, data, context=context)
            if not new_ids:
                return {'type': 'ir.actions.act_window_close'}
            if len(new_ids) <= 1:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name': _('Quotation'),
                    'res_id': new_ids and new_ids[0]
                }
            else:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name': _('Quotation'),
                    'res_id': new_ids
                }
            return value
