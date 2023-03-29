import itertools
import json
import datetime
import locale
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception
from werkzeug.exceptions import NotFound
from odoo.tools import float_round
import calendar


class ExportController(http.Controller):

    @http.route('/dashboard/sales/<bcsrf>', atype='http', auth='user', website=True)
    def my_template_controller(self, bcsrf, **kw):
        dashboard = request.env['sales.dashboard.config'].sudo().search(
            [('generate_token_link', '=', bcsrf)], limit=1)

        if dashboard:



            nowx = datetime.datetime.now()
            start_date = datetime.datetime(nowx.year, nowx.month, 1).date()
            # start_date = datetime(2023, 1, 1).date()
            end_date = nowx.date()

            working_days = []
            for count_day in dashboard.count_day:
                working_days.append(int(count_day.values_day))

            public_holidays = []
            for holidays_date in dashboard.public_holidays_id:
                holidays = holidays_date.public_holidays_date
                public_holidays.append(holidays)




            result_local = request.env['sale.order'].sudo().search(
                [('state', 'not in', ['cancel', 'draft']),
                 ('journal_sales_config_id', '=', dashboard.sales_local_type.id),
                 ('commitment_date', '>=', start_date),
                 ('commitment_date', '<=', end_date)] )

            result_export = request.env['sale.order'].sudo().search(
                [('state', 'not in', ['cancel', 'draft']),
                 ('journal_sales_config_id', '=', dashboard.sales_export_type.id),
                 ('commitment_date', '>=', start_date),
                 ('commitment_date', '<=', end_date)])

            result_marketing = request.env['sale.order'].sudo().search(
                [('state', 'not in', ['cancel', 'draft']),
                 ('journal_sales_config_id', '=', dashboard.sales_marketing_type.id),
                 ('commitment_date', '>=', start_date),
                 ('commitment_date', '<=', end_date)])

            last_day_of_month = calendar.monthrange(nowx.year, nowx.month)[1]
            end_date_mouth = datetime.datetime(nowx.year, nowx.month, last_day_of_month).date()
            holidays_count = request.env['sales.dashboard.config.holidays'].sudo().search(
                [
                    ('public_holidays_id', '=', dashboard.id),
                    ('public_holidays_date', '>=', start_date),
                    ('public_holidays_date', '<=', end_date_mouth)])



            # Render the template and return the response
            local_target = dashboard.sales_local_target
            export_target = dashboard.sales_export_target
            marketing_target = dashboard.sales_marketing_target





            local_total_thb = sum(result_local.mapped('x_studio_total_thb'))
            export_total_thb = sum(result_export.mapped('x_studio_total_thb'))
            marketing_total_thb = sum(result_marketing.mapped('x_studio_total_thb'))

            local_Goals_if = local_total_thb - local_target
            export_Goals_if = export_total_thb - export_target
            marketing_Goals_if = marketing_total_thb - marketing_target
            custom_class ='col-xl-6'
            if local_target>0 and export_target >0 and marketing_target>0:
                custom_class = 'col-xl-4'

            order_data = {
                'title': dashboard.name,
                'custom_class':custom_class,
                'orders_local': self.order_line_popular(result_local, dashboard.popular_products),
                'orders_export': self.order_line_popular(result_export, dashboard.popular_products),
                'orders_marketing': self.order_line_popular(result_marketing, dashboard.popular_products),

                'local_target_if':local_target,
                'export_target_if': export_target,
                'marketing_target_if': marketing_target,

                'local_target': self.convert_currency(local_target),
                'export_target': self.convert_currency(export_target),
                'marketing_target': self.convert_currency(marketing_target),

                'local_amount': self.convert_currency(local_total_thb),
                'export_amount': self.convert_currency(export_total_thb),
                'marketing_amount': self.convert_currency(marketing_total_thb),

                'local_Goals': self.convert_currency(local_Goals_if),
                'export_Goals': self.convert_currency(export_Goals_if),
                'marketing_Goals': self.convert_currency(marketing_Goals_if),

                'local_Goals_if': local_Goals_if,
                'export_Goals_if': export_Goals_if,
                'marketing_Goals_if': marketing_Goals_if,

                'auto_reload': dashboard.auto_reload,
                'holidays': len(holidays_count) ,
                'start_date': start_date.strftime('%B %d, %Y'),
                'end_date': end_date.strftime('%B %d, %Y'),
                'num_working_days': self.working_days(end_date, end_date_mouth, working_days, public_holidays)
            }

            return http.request.render('boxs_controller_api.my_template', order_data)
        else:
            raise NotFound()

    def order_line_popular(self, order_line, show_top=5):
        # order_lines = request.env['sale.order.line'].sudo().search([('order_id', '=', order_line.id)])
        # search for sale order lines and group by product_id while summing qty_delivered

        order_lines = request.env['sale.order.line'].sudo().read_group(
            domain=[('order_id', 'in', order_line.ids), ('product_id', '!=', False)],
            fields=['product_id', 'product_uom', 'qty_delivered'],
            groupby=['product_id', 'product_uom'],
            lazy=False
        )

        # create result dictionary
        result = []
        # add data to result
        for line in order_lines:
            product = request.env['product.product'].sudo().browse(line['product_id'][0])
            product_uom = request.env['uom.uom'].sudo().browse(line['product_uom'][0])
            my_string = product.default_code
            package_size = my_string.split(":")
            rounded_number = float_round(line['qty_delivered'], precision_digits=2)
            formatted_number = '{:,.2f}'.format(rounded_number)
            if len(package_size) >=2:
                package_size =package_size[1]
            else :
                package_size =""

            result.append({
                'product': product.name,
                'qty_delivered': formatted_number,
                'qty_sorted': rounded_number,
                'product_uom': product_uom.name,
                'package_size': package_size,
            })

        return sorted(result, key=lambda x: x['qty_sorted'], reverse=True)[:show_top]

    def convert_currency(self, valus, symbol=True):
        # locale.setlocale(locale.LC_ALL, 'th_TH')
        locale.setlocale(locale.LC_MONETARY, 'th_TH.UTF-8')
        return locale.currency(valus, symbol=symbol, grouping=True)

    def working_days(self, start_date, end_date, working_days, public_holidays):
        #nowx = datetime.datetime.now()
        # last_day_of_month = calendar.monthrange(nowx.year, nowx.month)[1]
        # # start_date = datetime(nowx.year, nowx.month, 1).date()
        # end_date = datetime.datetime(nowx.year, nowx.month, last_day_of_month).date()
        # working_days = [0, 1, 2, 3, 4]  # Monday to Friday

        num_working_days = 0
        current_date = start_date
        while current_date <= end_date:
            # Check if the current date is a public holiday
            if current_date in public_holidays:
                pass  # This day is a public holiday, do nothing
            # Check if the current date is a working day
            elif current_date.weekday() in working_days:
                num_working_days += 1
            # Otherwise, this day is a weekend, do nothing
            # Move to the next dayz
            current_date += datetime.timedelta(days=1)

        return num_working_days

