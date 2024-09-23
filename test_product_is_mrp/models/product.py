from odoo import api, models

# use the @api.constrains
# if it has the "Manufacturing" route, then update their names accordingly.
# if a product doesn't have any routes or if the "Manufacturing" route is removed after adding the tag.
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    @api.constrains('route_ids')
    def _update_product_name_with_mrp_tag(self):
        for rec in self:
            Manufacturing_Route = self.env['stock.route'].search([('name', '=', 'Manufacture')])
            if Manufacturing_Route in rec.route_ids:
                rec.name = "[MRP]"+ rec.name
            else:
                rec.name = rec.name.replace("[MRP]","")

