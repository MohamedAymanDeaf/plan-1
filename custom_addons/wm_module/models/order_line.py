from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
        domain="[('active','=',True), ('company_id','=', parent.company_id), ('job_id','=', parent.job_id)]"
    )

    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price', default=0.0)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = (line.quantity or 0.0) * (line.price_unit or 0.0)

    @api.onchange('part_id')
    def _onchange_part_id(self):
        for line in self:
            if line.part_id:
                line.price_unit = line.part_id.price or 0.0

    @api.constrains('quantity')
    def _check_quantity(self):
        for line in self:
            if line.quantity is None:
                continue
            if line.quantity <= 0:
                raise ValidationError("Quantity must be greater than 0.")
