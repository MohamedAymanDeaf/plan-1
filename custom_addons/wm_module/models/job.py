from odoo import models, fields, api

class Job(models.Model):
    _name = "job"
    _description = "Job"

    name = fields.Char(string="Name", required=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        index=True
    )

    order_line_ids = fields.One2many(
        comodel_name="order_line",
        inverse_name="job_id",
        string="Order Lines"
    )

    part_count = fields.Integer(
        string="Parts Count",
        compute="_compute_part_count",
        store=True
    )

    @api.depends("order_line_ids")
    def _compute_part_count(self):
        for rec in self:
            rec.part_count = len(rec.order_line_ids)
