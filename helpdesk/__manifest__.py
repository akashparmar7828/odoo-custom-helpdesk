{
    'name': 'helpdesk',
    'version': '1.0',
    'category': 'Service',
    'summary': 'Email based Helpdesk with Teams and Chatters',
    'description': 'Email based Helpdesk with Teams and Chatters',
    'author': 'Iprogrammer',
    'website': 'http://www.iprogrammer.com',
    'depends': ['mail', 'hr', 'account'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ticket_rules.xml',

        'views/team_views.xml',
        'views/stage_views.xml',
        'views/sla_views.xml',
        'data/stage_data.xml',
        'views/ticket_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
}
