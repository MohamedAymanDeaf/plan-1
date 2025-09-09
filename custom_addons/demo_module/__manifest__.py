{
    'name': 'Demo Module',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'Simple demo module',
    'description': 'This is a demo module for testing.',
    'author': 'Mohamed',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/demo_menu.xml',
    ],

    'installable': True,
    'application': True,
}
