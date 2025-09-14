from odoo import models, fields

class OrderStatusWizard(models.TransientModel):
    _name = 'order.status.wizard'
    _description = 'Wizard to change Order Status'

    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string='New Status', required=True)
    order_id = fields.Many2one('order', string='Order')

    def action_apply(self):
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            orders = self.env['order'].browse(active_ids)
            orders.write({'state': self.status})
