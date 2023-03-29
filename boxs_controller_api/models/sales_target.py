from odoo import api, fields, models, SUPERUSER_ID, tools, _lt, _
import hashlib
import datetime
import random
import string


class MyWeekdaysLine(models.Model):
    _name = 'sales.dashboard.config.weekdays'
    _description = "sales dashboard config weekdays"
    name = fields.Char(string='public holidays name', requests=True)
    values_day = fields.Char(string='public holidays date', requests=True)

class sales_target(models.Model):
    _name = 'sales.dashboard.config'
    _description = 'sale dashboard config'
    name = fields.Char('config  name', required=True, default='New')
    generate_token_link = fields.Char('Token  Reference', required=True, default='New')
    sales_local_target = fields.Float(string="Sales local monthly target", required=True)
    sales_export_target = fields.Float(string="Sales Export monthly target", required=True)
    sales_marketing_target = fields.Float(string="Sales marketing monthly target", required=True)
    sales_local_type = fields.Many2one('btl.journal.sales.order.config', string='Sales local Type',
                                       required=True)
    sales_export_type = fields.Many2one('btl.journal.sales.order.config', string='Sales export Type',
                                        required=True)
    sales_marketing_type = fields.Many2one('btl.journal.sales.order.config', string='Sales marketing Type',
                                        required=True)
    auto_reload = fields.Integer(string='auto reload Minutes',
                                 required=True, default=5)
    popular_products = fields.Integer(string='Show TOP Popular Products ',
                                 required=True, default=5)


    count_day =fields.Many2many( 'sales.dashboard.config.weekdays', string="Count Day", requests=True  )

    public_holidays_id = fields.One2many('sales.dashboard.config.holidays', 'public_holidays_id',
                                         string='public holidays')

    @api.model
    def create(self, vals):
        rand_num = random.randint(10, 32)
        if vals.get('name', 'New') == 'New':
            vals['name'] ="Dashbord Monthly Target "
            vals['generate_token_link'] = self.generate_token(rand_num)
        return super(sales_target, self).create(vals)

    def act_generate_token(self):
        self.generate_token_link = self.generate_token(10)

    def generate_token(self, length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

    def open_my_website(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        return {
            'type': 'ir.actions.act_url',
            'url': base_url + "/dashboard/sales/" + self.generate_token_link,
            'target': 'new',
        }


class MyHolidayslineLine(models.Model):
    _name = 'sales.dashboard.config.holidays'
    _description = "sales dashboard config holidaysline"
    name = fields.Char(string='public holidays name', requests=True)
    public_holidays_date = fields.Date(string='public holidays date', requests=True)
    sequence = fields.Integer()
    public_holidays_id = fields.Many2one('sales.dashboard.config', string='public holidays')

    _sql_constraints = [
        ('uniq_holiday_name', 'unique(public_holidays_date)', 'Holiday date must be unique!')
    ]
