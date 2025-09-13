from odoo import models, fields

class OrderLine(models.Model):
    _name = 'order_line'
    _description = 'Order Line'

    order_id = fields.Many2one('order', string='Order', ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', related="order_id.company_id", store=True)
    job_id = fields.Many2one('job', string='Job', related="order_id.job_id", store=True)

    part_id = fields.Many2one(
        'part',
        string='Part',
        domain="[('active','=', True), ('company_id','=', company_id), ('job_id','=', job_id)]"
    )
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price', default=0.0)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
