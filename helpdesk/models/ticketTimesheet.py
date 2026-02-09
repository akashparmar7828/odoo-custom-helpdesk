from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HelpdeskTicketTimesheet(models.Model):
    _name = "custom.helpdesk.ticket.timesheet"
    _description = "Ticket Timesheet"
    _order = "date desc"

    ticket_id = fields.Many2one("custom.helpdesk.ticket", required=True, ondelete="cascade")
    partner_id = fields.Many2one(related="ticket_id.partner_id", store=True)
    use_time_billing = fields.Boolean(related="ticket_id.use_time_billing", store=True)
    date = fields.Date(default=fields.Date.today, required=True)
    employee_id = fields.Many2one("hr.employee", required=True, default=lambda self: self.env.user.employee_id)
    description = fields.Char(required=True)
    time_spent = fields.Float(string="Hours", required=True)
    billable = fields.Boolean(default=True)
    hourly_rate = fields.Float(string="Hourly Rate")
    amount = fields.Float(string="Bill Amount", compute="_compute_amount", store=True)
    invoice_id = fields.Many2one("account.move", readonly=True)

    @api.depends("time_spent", "hourly_rate", "billable", "use_time_billing")
    def _compute_amount(self):
        for rec in self:
            if rec.billable and rec.use_time_billing:
                rec.amount = rec.time_spent * rec.hourly_rate
            else:
                rec.amount = 0

    @api.constrains("time_spent")
    def _check_time(self):
        for rec in self:
            if rec.time_spent <= 0:
                raise ValidationError("Time must be greater than 0")

    @api.onchange("employee_id")
    def _onchange_employee_rate(self):
        for rec in self:
            if rec.employee_id and not rec.hourly_rate:
                rec.hourly_rate = getattr(rec.employee_id, "hourly_rate", 0)

    def action_create_invoice(self):
        self.ensure_one()
        if not self.use_time_billing:
            raise ValidationError("Billing is disabled for this team")
        if not self.billable:
            raise ValidationError("Timesheet is not billable")
        if not self.partner_id:
            raise ValidationError("Customer is required")
        if self.invoice_id:
            raise ValidationError("Invoice already created")

        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner_id.id,
            "invoice_line_ids": [(0, 0, {
                "name": self.description,
                "quantity": self.time_spent,
                "price_unit": self.hourly_rate,
            })]
        })

        self.invoice_id = invoice.id

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": invoice.id,
            "view_mode": "form"
        }

