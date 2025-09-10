from odoo import models, fields, api

class Order(models.Model):
    _name = 'order'
    _description = 'Order'
    _rec_name = 'name'

    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('order') or 'New'
    )
    job_id = fields.Many2one('job', string='Job')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    line_ids = fields.One2many('order_line', 'order_id', string='Order Lines')

    total_quantity = fields.Float(string='Total Quantity', compute='_compute_totals', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_totals', store=True)

    @api.depends('line_ids.quantity', 'line_ids.subtotal')
    def _compute_totals(self):
        for order in self:
            order.total_quantity = sum(line.quantity for line in order.line_ids)
            order.total_amount = sum(line.subtotal for line in order.line_ids)
