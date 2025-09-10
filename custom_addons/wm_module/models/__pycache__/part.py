from odoo import models, fields

class Part(models.Model):
    _name = 'part'
    _description = 'Part'

    name = fields.Char(string='Part Name', required=True)
    code = fields.Char(string='Code')
    job_id = fields.Many2one('job', string='Job')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
