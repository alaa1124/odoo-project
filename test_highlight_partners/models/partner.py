from odoo import models, api,fields

# Step-by-step thought process:
# Define the data model for storing highlighted partners.
# Create a website snippet template. I try it through website builder
# Implement JavaScript functionality for the snippet.
# I didnot have engouph information, but I’ve studied OWL for one month, which will help you with this step, NOW I am in step of learn React JS
# Configure the snippet in the website builder.
# Add necessary XML files for the module structure. ---> i did it by implementing a button (get_highlighted_partners) to retrieve data from the highlight_partner field.


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Define the data model for storing highlighted partners.
    highlight_partner = fields.Boolean(string="Highlight Partner", default=False)

    def get_highlighted_partners(self):
        highlighted_partners = self.search([('highlight_partner', '=', True)])

        if highlighted_partners:
            partner_names = "\n".join(highlighted_partners.mapped('name'))
            message = f"The following partners are highlighted:\n{partner_names}"

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Highlighted Partners',
                    'message': message,
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Highlighted Partners',
                    'message': 'No partners are highlighted.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
