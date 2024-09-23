from odoo import _, api, fields, models
from lxml import etree
from odoo import models, api
from odoo.exceptions import ValidationError, AccessError

# Step-by-step thought process:

# get_view to make the salesperson field read-only for non-managers, and enforce this restriction with the check_salesperson_change method.
# a default sales team for users by defining _default_team and applying it during record creation.
# access restrictions in the write method, preventing salespersons from editing orders outside their sales team.
# security groups for managers and salespersons with appropriate access rights in XML, and use record rules to enforce team-based access control.
# Python constraints to enforce restrictions in the backend, ensuring both UI and logic are aligned.
class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "Sale Order Inherit"

    total_quantity = fields.Float(
        compute='_compute_total_quantity'
    )


    @api.depends('order_line')
    def _compute_total_quantity(self):
        for rec in self:
            rec.total_quantity = sum(rec.order_line.mapped('product_uom_qty'))

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super(SaleOrder, self)._get_view(view_id, view_type, **options)
        if view_type == 'form' and not self.env.user.has_group('sales_team.group_sale_manager'):
            for node in arch.xpath("//field[@name='user_id']"):
                node.set('readonly', '1')
        return arch, view

    @api.constrains('user_id')
    def check_salesperson_change(self):
        for rec in self:
            if not self.env.user.has_group('sales_team.group_sale_manager'):
                raise ValidationError(_("Only managers are allowed to change the salesperson."))

    @api.model
    def _default_team(self):
        return self.env.user.sale_team_id

    @api.model
    def create(self, vals):
        if not vals.get('team_id'):
            print("inside create")
            vals['team_id'] = self.env.user.sale_team_id.id
        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        if self.env.user.has_group('so_po_edits.group_salesperson'):
            print("inside write")
            if any(order.team_id != self.env.user.sale_team_id for order in self):
                raise AccessError("You cannot modify orders outside your sales team.")
        return super(SaleOrder, self).write(vals)
