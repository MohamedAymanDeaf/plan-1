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
        index=True,
        default='New',
        tracking=True
    )
    job_id = fields.Many2one('job', string='Job', tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, tracking=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        index=True,
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
        ('invoiced', 'Invoiced'),
    ], string='Status', default='draft', tracking=True)

    # invoices link
    invoice_ids = fields.One2many('account.move', 'wm_order_id', string='Invoices')
    invoice_count = fields.Integer(compute='_compute_invoice_count', string="Invoice Count")

    @api.depends('line_ids.quantity', 'line_ids.subtotal')
    def _compute_totals(self):
        for order in self:
            order.total_quantity = sum(line.quantity for line in order.line_ids)
            order.total_amount = sum(line.subtotal for line in order.line_ids)

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for order in self:
            order.invoice_count = len(order.invoice_ids)

    _sql_constraints = [
        ('unique_order_name', 'unique(name)', 'Order name must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('order') or 'New'
        return super(Order, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('order') or 'New'
        return super(Order, self).write(vals)

    def action_autonumber_old_orders(self):
        for order in self.search([('name', '=', 'New')]):
            order.name = self.env['ir.sequence'].next_by_code('order') or 'New'

    @api.model
    def cron_auto_close_old_orders(self):
        limit_date = fields.Date.today() - timedelta(days=30)
        old_orders = self.search([
            ('date', '<', limit_date),
            ('state', 'in', ['draft', 'confirmed'])
        ])
        for order in old_orders:
            order.state = 'cancelled'

    def action_create_invoice(self):
        invoices = self.env['account.move']
        for order in self:
            if not order.line_ids:
                continue
            move_vals = {
                'move_type': 'out_invoice',
                'invoice_date': fields.Date.context_today(self),
                'partner_id': order.job_id.id if order.job_id else False,
                'wm_order_id': order.id,
                'invoice_line_ids': [],
            }
            for line in order.line_ids:
                income_account = self.env['account.account'].search(
                    [('user_type_id.type', '=', 'income')], limit=1
                )
                line_vals = (0, 0, {
                    'name': line.part_id.name or 'Line',
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'account_id': income_account.id if income_account else False,
                })
                move_vals['invoice_line_ids'].append(line_vals)
            invoice = self.env['account.move'].create(move_vals)
            invoices |= invoice
        if invoices:
            if len(invoices) == 1:
                invoice = invoices[0]
                return {
                    'name': 'Invoice',
                    'view_mode': 'form',
                    'res_model': 'account.move',
                    'res_id': invoice.id,
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                }
            else:
                return {
                    'name': 'Invoices',
                    'res_model': 'account.move',
                    'view_mode': 'list,form',
                    'type': 'ir.actions.act_window',
                    'domain': [('id', 'in', invoices.ids)],
                    'target': 'current',
                }
        return True

    def action_open_invoices(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
            'context': {'default_wm_order_id': self.id},
            'target': 'current',
        }

    def action_open_status_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Change Status',
            'res_model': 'order.status.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }


class AccountMove(models.Model):
    _inherit = 'account.move'

    wm_order_id = fields.Many2one('order', string='Order')
