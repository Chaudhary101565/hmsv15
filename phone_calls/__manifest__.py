{
    'name': 'Phone Calls',
    'version': '16.0',
    'summary': 'Record Phone Calls Duration',
    'description': 'Record Phone Calls Durations',
    'category': 'Custom',
    'author': 'Custom',
    'website': 'http://www.custom.com',
    'license': 'OPL-1',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/phone_calls.xml',
        'menu/menu.xml'
    ],
    'installable': True,
    'auto_install': False,
}
