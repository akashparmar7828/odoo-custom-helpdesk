from odoo import models, fields
class HelpdeskSLA(models.Model):
    _name = 'custom.helpdesk.sla'
    _description = 'Helpdesk SLA'
    name = fields.Char(required=True)
    team_id = fields.Many2one('custom.helpdesk.team', required=True)
    priority = fields.Selection([
        ('0','Low'),
        ('1','Medium'),
        ('2','High'),
        ('3','Critical')
    ])
    reach_stage_id = fields.Many2one('custom.helpdesk.stage')
    hours = fields.Float(required=True)
