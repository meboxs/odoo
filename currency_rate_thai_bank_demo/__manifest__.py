# -*- coding: utf-8 -*-
{
    'name': "Currency Rates of Bank Thailand DEMO",  # Module title
    'summary': "Currency Rates of Bank Thailand DEMO",  # Module subtitle phrase
    'description': """

==============
Description related to Currency Rates of Bank Thailand DEMO.
    """,
    'author': "Boxs.Me",
    'website': "http://www.boxs.me",
    'images': ['static/description/cover.png'],
    'category': 'Tools',
    'version': '14.0.1',
     "sequence": 0,
    "currency": "USD",
    "price": "0.0",
    "license": "LGPL-3",
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
