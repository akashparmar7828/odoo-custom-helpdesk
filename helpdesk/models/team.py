from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class HelpdeskTeam(models.Model):
    _name = 'custom.helpdesk.team'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Helpdesk Team'
    _order = "sequence, name"

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True, tracking=True)
    description = fields.Text()
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    visibility = fields.Selection([
        ('private', 'Only Team Members'),
        ('company', 'All Internal Users'),
        ('assigned_only', 'Assigned User Only'),
    ], default='company')
    member_ids = fields.Many2many('res.users')
    assign_method = fields.Selection([
        ('manual', 'Manual'),
        ('least_loaded', 'Automatic Assignment')
    ], default='manual')
    use_alias = fields.Boolean()
    alias_name = fields.Char()
    alias_id = fields.Many2one('mail.alias', ondelete='set null')
    alias_email = fields.Char(related="alias_id.display_name", string="Email Alias")
    use_sla = fields.Boolean()
    working_hours_id = fields.Many2one('resource.calendar')
    use_rating = fields.Boolean()
    use_timesheet = fields.Boolean(string="Timesheets", help="Track time spent on tickets")
    use_time_billing = fields.Boolean(string="Time Billing", help="Bill time spent on tickets to customers")

    def _create_or_update_alias(self):
        model = self.env['ir.model']._get('custom.helpdesk.ticket')
        for team in self:
            if not team.alias_name:
                raise ValidationError("Alias name required when Email Alias enabled")

            alias_name = re.sub(r'[^a-z0-9]', '', team.alias_name.lower())

            existing = self.env['mail.alias'].search([
                ('alias_name', '=', alias_name),
                ('id', '!=', team.alias_id.id if team.alias_id else 0)
            ], limit=1)

            if existing:
                raise ValidationError("Alias already exists")

            vals = {
                'alias_name': alias_name,
                'alias_model_id': model.id,
                'alias_defaults': {'team_id': team.id}
            }

            if team.alias_id:
                team.alias_id.write(vals)
            else:
                team.alias_id = self.env['mail.alias'].create(vals)

    @api.model_create_multi
    def create(self, vals_list):
        teams = super().create(vals_list)
        for team in teams:
            if team.use_alias:
                team._create_or_update_alias()
        return teams

    def write(self, vals):
        res = super().write(vals)
        for team in self:
            if team.use_alias and ('alias_name' in vals or 'use_alias' in vals or not team.alias_id):
                team._create_or_update_alias()

            if not team.use_alias and team.alias_id:
                team.alias_id.unlink()
                team.alias_id = False
        return res
