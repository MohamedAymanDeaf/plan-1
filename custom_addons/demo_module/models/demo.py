from odoo import models, fields

class Demo(models.Model):
    _name = 'demo.model'
    _description = 'Demo Model'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
