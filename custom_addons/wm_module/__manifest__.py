{
    'name': 'Work Management',
    'version': '1.0',
    'summary': 'Jobs, Parts and Orders (minimal)',
    'category': 'Operations',
    'author': 'Mohamed',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_wm.xml',
        'views/wm_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
