from odoo import models, fields
class HelpdeskStage(models.Model):
    _name = 'custom.helpdesk.stage'
    _description = 'Ticket Stage'
    _order = 'sequence'
    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    fold = fields.Boolean()
