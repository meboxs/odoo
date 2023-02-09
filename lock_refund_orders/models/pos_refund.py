from odoo import api, fields, models, tools, _


class ModelposName(models.Model):
    _inherit = "pos.order"
    lock_refund = fields.Char(string='sale contacts type')

    # #
    # @api.model
    # def create(self, values):
    #     try:
    #         if values['pos_reference']:
    #             refund_orders = self.env['pos.order']
    #             total_len = refund_orders.search_count(
    #                 [('pos_reference', '=', self.pos_reference)])
    #             if total_len > 1:
    #                 pos_reference_name = refund_orders.search(
    #                     [('pos_reference', '=', self.pos_reference), ('name', '!=', self.name)], limit=1)
    #                 return self.show_notification("คุณได้ทำการคืนเงินในระบบแล้ว !!!",
    #                                               "คำสั่งซื้อ :" + pos_reference_name.name + " มีการทำ refund ไปแล้วกรุณตรวจสอบ refund :" + self.name,
    #                                               "warning")
    #             else:
    #                 res = super(ModelposName, self).create(values)
    #                 return res
    #     except:
    #         res = super(AccountMoveNew, self).create(values)
    #         return res

    def refund(self):
        """Create a copy of order  for refund order"""
        refund_orders = self.env['pos.order']
        total_len = refund_orders.search_count(
            [('pos_reference', '=', self.pos_reference)])
        if total_len > 1:
            pos_reference_name = refund_orders.search(
                [('pos_reference', '=', self.pos_reference), ('name', '!=', self.name)], limit=1)
            return self.show_notification("คุณได้ทำการคืนเงินในระบบแล้ว !!!",
                                          "คำสั่งซื้อ :" + pos_reference_name.name + " มีการทำ refund ไปแล้วกรุณตรวจสอบ refund :" + self.name,
                                          "warning")
        else:

            """Create a copy of order  for refund order"""
            for order in self:
                # When a refund is performed, we are creating it in a session having the same config as the original
                # order. It can be the same session, or if it has been closed the new one that has been opened.
                current_session = order.session_id.config_id.current_session_id
                if not current_session:
                    raise UserError(_('To return product(s), you need to open a session in the POS %s',
                                      order.session_id.config_id.display_name))
                refund_order = order.copy(
                    order._prepare_refund_values(current_session)
                )
                for line in order.lines:
                    PosOrderLineLot = self.env['pos.pack.operation.lot']
                    for pack_lot in line.pack_lot_ids:
                        PosOrderLineLot += pack_lot.copy()
                    line.copy(line._prepare_refund_data(refund_order, PosOrderLineLot))
                refund_orders |= refund_order

            return {
                'name': _('Return Products'),
                'view_mode': 'form',
                'res_model': 'pos.order',
                'res_id': refund_orders.ids[0],
                'view_id': False,
                'context': self.env.context,
                'type': 'ir.actions.act_window',
                'target': 'current',
            }

    def show_notification(self, title, Message, type, sticky=True):
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': (title),
                'message': Message,
                'type': type,  # types: success,warning,danger,info
                'sticky': sticky,  # True/False will display for few seconds if false
            },
        }
        return notification
