from odoo import models, fields, api

class OrderLine(models.Model):
    _name = 'order_line'
    _description = 'Order Line'

    order_id = fields.Many2one(
        'order',
        string='Order',
        required=True,
        ondelete='cascade'
    )

    job_id = fields.Many2one(
        'job',
        string='Job',
        related='order_id.job_id',
        store=True,
        readonly=True
    )

    part_id = fields.Many2one(
        'part',
        string='Part',
        required=True,
        domain="[('active','=',True), ('company_id','=', order_id.company_id), ('job_id','=', order_id.job_id)]"
    )

    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price', default=0.0)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = (line.quantity or 0.0)
