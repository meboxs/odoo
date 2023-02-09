from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = "pos.order"
    lock_refund = fields.Char(string='sale contacts type')
    #
    # @api.model
    # def create(self, values):
    #     try:
    #         if values['move_type']:
    #             if values['move_type'] in ('out_invoice', 'out_refund'):
    #                 sales_order = self.env['sale.order'].search([('name', '=', values['invoice_origin'])], limit=1)
    #                 if sales_order:
    #                     values['journal_id'] = sales_order.journal_sales_config_id.journal_for_contacts.id
    #         # self.message_post(body=self.move_type)
    #         res = super(AccountMoveNew, self).create(values)
    #         return res
    #     except:
    #         res = super(AccountMoveNew, self).create(values)
    #         return res

    def refund(self):
        """Create a copy of order  for refund order"""
        refund_orders = self.env['pos.order']

        total_len = refund_orders.search_count(
            [('pos_reference', '=', self.pos_reference), ('pos_reference', '=', self.pos_reference)])
        if total_len >1:

            pos_reference_name = refund_orders.search(
                [('pos_reference', '=', self.pos_reference), ('name', '!=', self.name)], limit=1)
            return self.show_notification("คุณได้ทำการคืนเงินในระบบแล้ว !!!",
                                          "คำสั่งซื้อ :" + self.name + " มีการทำ refund ไปแล้วกรุณตรวจสอบ refund :" + pos_reference_name.name,
                                          "warning")

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
