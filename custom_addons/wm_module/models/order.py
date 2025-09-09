from odoo import models, fields, api

class WMOrder(models.Model):
    _name = 'wm.order'
    _description = 'Work Order'
    _rec_name = 'name'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default='New')
    job_id = fields.Many2one('wm.job', string='Job', required=True)
    part_ids = fields.Many2many('wm.part', string='Parts')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    part_count = fields.Integer(string='Parts Count', compute='_compute_part_count')

    @api.depends('part_ids')
    def _compute_part_count(self):
        for rec in self:
            rec.part_count = len(rec.part_ids)

    @api.model
    def create(self, vals):
        # يستخدم الـ sequence لتعريف رقم الأوردر
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('wm.order') or 'New'
        return super(WMOrder, self).create(vals)
