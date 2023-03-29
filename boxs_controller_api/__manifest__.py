{
    'name': 'My Module Boxs',
    'version': '1.0',
    'summary': 'My module summary',
    'description': 'My module description',
    'author': 'Boxs Me.',
    'website': 'http://boxs.me',
    'depends': ['base', 'sale', 'journal_sales_order_by_contacts'],
    'data': [
      
        'template/my_template.xml',
        'views/sales_dashboard_config.xml',
        'security/res_currency_rate_provider.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
    ],
    'qweb': [
        # Other QWeb templates here
    ],
    'images': [
        # Module images here
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_frontend': [
            'boxs_controller_api/static/**/*',
        ],
    },
}
