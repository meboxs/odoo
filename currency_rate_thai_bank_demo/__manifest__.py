# -*- coding: utf-8 -*-
{
    'name': "Currency Rates of Bank Thailand DEMO",  # Module title
    'summary': "Currency Rates of Bank Thailand DEMO",  # Module subtitle phrase
    'description': """

==============
Description related to Currency Rates of Bank Thailand DEMO.
    """,
    'author': "boxs.me",
    'website': "http://www.boxs.me",
    'category': 'Tools',
    'version': '15.0.1',
    'installable': True,
    'application': True,
    'auto_install': False,
    'depends': ['account', 'base'],
    'data': [  'views/CurrencyThailandConfig.xml',
             'wizard/wizard_update_currency_rates.xml',
             'security/res_currency_rate_provider.xml',
             'security/ir.model.access.csv',
             ],

}
