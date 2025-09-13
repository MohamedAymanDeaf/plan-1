from odoo import models, fields, api
from datetime import timedelta

class Order(models.Model):
    _name = 'order'
    _description = 'Order'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('order') or 'New',
        tracking=True
    )
    job_id = fields.Many2one('job', string='Job', tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, tracking=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        tracking=True
    )

    line_ids = fields.One2many('order_line', 'order_id', string='Order Lines')

    total_quantity = fields.Float(
        string='Total Quantity',
        compute='_compute_totals',
        store=True,
        tracking=True
    )
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_totals',
        store=True,
        tracking=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    @api.depends('line_ids.quantity', 'line_ids.subtotal')
    def _compute_totals(self):
        for order in self:
            order.total_quantity = sum(line.quantity for line in order.line_ids)
            order.total_amount = sum(line.subtotal for line in order.line_ids)

    _sql_constraints = [
        ('unique_order_name', 'unique(name)', 'Order name must be unique!')
    ]

    # -------- Server Action: Autonumber for older orders --------
    def action_autonumber_old_orders(self):
        """Assign sequence numbers to old orders without a proper name"""
        for order in self.search([('name', '=', 'New')]):
            order.name = self.env['ir.sequence'].next_by_code('order') or 'New'

    # -------- Cron Job: Auto-close orders older than 30 days --------
    @api.model
    def cron_auto_close_old_orders(self):
        """Close orders older than 30 days that are still in draft/confirmed"""
        limit_date = fields.Date.today() - timedelta(days=30)
        old_orders = self.search([
            ('date', '<', limit_date),
            ('state', 'in', ['draft', 'confirmed'])
        ])
        for order in old_orders:
            order.state = 'cancelled'
