from odoo import models, fields, api

class WMJob(models.Model):
    _name = 'wm.job'
    _description = 'Work Job'

    name = fields.Char(string='Job Name', required=True)
    description = fields.Text(string='Description')
    part_ids = fields.One2many('wm.part', 'job_id', string='Parts')
    part_count = fields.Integer(string='Parts Count', compute='_compute_part_count')

    @api.depends('part_ids')
    def _compute_part_count(self):
        for rec in self:
            rec.part_count = len(rec.part_ids)
