# from odoo import api, fields, models
#
#
# class ProjectTask(models.Model):
#     _inherit = 'project.task'
#
#     _order = 'order_code'
#
#     code = fields.Char()
#     order_code = fields.Char(compute='_compute_order_code', store=True)
#
#     @api.depends('code', 'parent_id')
#     def _compute_order_code(self):
#         for rec in self:
#             result = rec.code or ''
#             parent = rec.parent_id
#             while parent:
#                 result = f'{parent.code}.{result}'
#                 parent = parent.parent_id
#             rec.order_code = result
