# models/order_status_wizard.py
from odoo import models, fields, api


class OrderStatusWizard(models.TransientModel):
    _name = 'order.status.wizard'
    _description = 'Wizard to change Order Status'

    order_id = fields.Many2one('order', string='Order')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('invoiced', 'Invoiced'),
    ], string='New Status', required=True)

    def action_apply(self):
        active_ids = self.env.context.get('active_ids') or [self.order_id.id] if self.order_id else []
        if active_ids:
            orders = self.env['order'].browse(active_ids)
            orders.write({'state': self.status})
        return {'type': 'ir.actions.act_window_close'}
