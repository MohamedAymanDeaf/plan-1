{
    'name': 'Work Management',
    'version': '1.0',
    'summary': 'Jobs, Parts, Orders with lines (wm_module) - Odoo 18',
    'category': 'Operations',
    'author': 'Mohamed',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_wm.xml',
        'views/wm_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
