from odoo import models, fields, api
from datetime import timedelta
import math

class HelpdeskTicket(models.Model):
    _name = 'custom.helpdesk.ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Helpdesk Ticket"
    _order = "priority desc, sla_deadline asc"

    name = fields.Char(required=True, tracking=True)
    description = fields.Text()
    team_id = fields.Many2one('custom.helpdesk.team', required=True)
    company_id = fields.Many2one('res.company', related='team_id.company_id', store=True, readonly=True)
    user_id = fields.Many2one('res.users', tracking=True)
    partner_id = fields.Many2one('res.partner')
    phone = fields.Char(related='partner_id.phone')
    team_visibility = fields.Selection(related="team_id.visibility", store=True)
    use_timesheet = fields.Boolean(related="team_id.use_timesheet", store=True)
    use_time_billing = fields.Boolean(related="team_id.use_time_billing", store=True)
    timesheet_ids = fields.One2many("custom.helpdesk.ticket.timesheet", "ticket_id", string="Timesheets")
    stage_id = fields.Many2one(
        'custom.helpdesk.stage',
        tracking=True,
        group_expand='_read_group_stage_ids',
        default=lambda self: self.env['custom.helpdesk.stage'].search([], order="sequence", limit=1)
    )
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical')
    ], default='1', tracking=True)
    sla_deadline = fields.Datetime(tracking=True)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return stages.search([], order='sequence')

    def _apply_sla(self):
        for ticket in self:
            sla = self.env['custom.helpdesk.sla'].search([
                ('team_id', '=', ticket.team_id.id),
                ('priority', '=', ticket.priority)
            ], limit=1)

            if not sla:
                sla = self.env['custom.helpdesk.sla'].search([
                    ('team_id', '=', ticket.team_id.id),
                    ('priority', '=', False)
                ], limit=1)

            hours = sla.hours if sla else 24
            ticket.sla_deadline = fields.Datetime.now() + timedelta(hours=hours)

    def _assign_least_loaded_user(self):
        members = self.team_id.member_ids
        if not members:
            return

        workload = {}
        for user in members:
            workload[user] = self.search_count([
                ('user_id', '=', user.id),
                ('stage_id.fold', '=', False)
            ])

        self.user_id = min(workload, key=workload.get)

    def action_done(self):
        done_stage = self.env['custom.helpdesk.stage'].search([
            ('name', '=', 'Done')
        ], limit=1)

        if done_stage:
            self.stage_id = done_stage.id

    def write(self, vals):
        res = super().write(vals)

        if vals.get('user_id'):
            assigned_stage = self.env['custom.helpdesk.stage'].search([
                ('name', '=', 'Assigned')
            ], limit=1)

            for ticket in self:
                if assigned_stage:
                    ticket.stage_id = assigned_stage.id

        return res

    @api.model
    def create(self, vals):
        ticket = super().create(vals)

        if ticket.team_id.use_sla:
            ticket._apply_sla()

        if ticket.team_id.assign_method == 'least_loaded':
            ticket._assign_least_loaded_user()

        if ticket.user_id:
            assigned_stage = self.env['custom.helpdesk.stage'].search([
                ('name', '=', 'Assigned')
            ], limit=1)

            if assigned_stage:
                ticket.stage_id = assigned_stage.id

        return ticket
