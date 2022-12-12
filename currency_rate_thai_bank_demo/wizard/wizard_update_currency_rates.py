import http.client
import json
import datetime
from odoo import api, fields, models, tools, _lt


# https://stackoverflow.com/questions/64520995/odoo-14-add-a-section-functionality-in-tree-view
# https://www.cybrosys.com/blog/how-to-create-user-notification-in-odoo-14
# How to Create User Notification in Odoo 14
class ChangeState(models.TransientModel):
    _name = 'res.currency.rate.thailand.config.state'
    _description = 'Change the state of sale order'
    name = fields.Many2one('res.currency.rate.thailand.config', string='Update Config', required=True)
    date_start = fields.Date(string='Start Date', default=datetime.date.today() - datetime.timedelta(days=5))
    date_end = fields.Date(string='End Date', default=fields.Date.today)

    def update_state_currency(self):
        active_currencies = self.env['res.company'].search([('id', '=', self.name.company_id.id)])
        Currency = self.env['res.currency']
        CurrencyRate = self.env['res.currency.rate']
        CurrencyRateConfig = self.env['res.currency.rate.thailand.config.line']

        start_period = self.date_start
        end_period = self.date_end
        Company_id = active_currencies.id

        try:
            conn = http.client.HTTPSConnection("apigw1.bot.or.th")
            api_bot_thailand = 'e4807974-ebf6-496b-a964-b501d1786e26'
            headers = {'X-IBM-Client-Id': api_bot_thailand}
            urlx = "/bot/public/Stat-ExchangeRate/v2/DAILY_AVG_EXG_RATE/"
            urlx2 = "?start_period=" + str(start_period.strftime("%Y-%m-%d")) + "&end_period=" + str(
                end_period.strftime("%Y-%m-%d"))
            conn.request("GET", urlx + urlx2, headers=headers)
            res = conn.getresponse()
            data = res.read()
            thb = json.loads(data)

            for currency_json in thb['result']['data']['data_detail']:
                currency_name = currency_json['currency_id']
                currency_object = Currency.search(
                    [('name', '=', currency_json['currency_id']), ('active', '=', 'true')])
                if currency_object:
                    CurrencyConfig = CurrencyRateConfig.search(
                        [('name', '=', currency_object.id), ('config_id', '=', self.name.id)])
                    if CurrencyConfig:

                        rate_api = currency_json[CurrencyConfig.api_fields]
                        currency_rate = CurrencyConfig.currency_exchange_rate
                        rate_value = float(currency_rate) / float(rate_api)

                        already_existing_rate = self.env['res.currency.rate'].search(
                            [('name', '=', currency_json['period']),
                             ('currency_id', '=', currency_object.id), ('company_id', '=', Company_id)])

                        if already_existing_rate:
                            already_existing_rate.write({'rate': float(rate_value)})
                        else:
                            CurrencyRate.create(
                                {'currency_id': currency_object.id, 'rate': float(rate_value),
                                 'name': currency_json['period'],
                                 'company_id': Company_id})

            mess = 'Update Currency Rates Start \n' + str(start_period.strftime("%Y-%m-%d"))
            mess += ' To ' + str(end_period.strftime("%Y-%m-%d")) + ' Success!!'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': mess,
                    'type': 'rainbow_man',
                }
            }
        except Exception as e:
            # connection error, the request wasn't successful
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('warning'),
                    'message': e,
                    'type': 'warning',  # types: success,warning,danger,info
                    'sticky': True,  # True/False will display for few seconds if false
                },
            }
            return notification
