from odoo import fields, models, api


# https://stackoverflow.com/questions/64520995/odoo-14-add-a-section-functionality-in-tree-view


class CurrencyThailandConfig(models.Model):
    _name = "res.currency.rate.thailand.config"
    _description = 'Foreign Exchange Rates of Thailand'
    name = fields.Char(string="Config Name", required=True)
    config_line_id = fields.One2many('res.currency.rate.thailand.config.line', 'config_id', string='currency rate')
    company_id = fields.Many2one('res.company', string='company', required=True , default=lambda self: self.env.company)


class MyCurrencyLine(models.Model):
    _name = "res.currency.rate.thailand.config.line"
    _description = "currency rate thailand config line "
    name = fields.Many2one('res.currency', 'currency name', requests=True)
    config_id = fields.Many2one('res.currency.rate.thailand.config', 'Lines Model')
    currency_exchange_rate = fields.Float(string='currency exchange rate', default='1', requests=True)
    api_fields = fields.Selection([
        ('buying_sight', 'Average Sight Bill'),
        ('buying_transfer', 'Average Transfer'),
        ('selling', 'Average Selling Rates'),
        ('mid_rate', 'mid_rate'),
    ], default='selling', string='Currency mapping to API fields', requests=True,
        help="Amount untaxed plus insurance percentage.")
    sequence = fields.Integer()
