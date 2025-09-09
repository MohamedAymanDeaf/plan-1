from odoo import models, fields

class WMPart(models.Model):
    _name = 'wm.part'
    _description = 'Work Part'

    name = fields.Char(string='Part Name', required=True)
    code = fields.Char(string='Code')
    job_id = fields.Many2one('wm.job', string='Job')
