from odoo import models, fields, api

# Step-by-step thought process:

# invoiced_notification_sent to track whether the notification has been sent for each sale order.(Boolean)
# _compute_invoice_status, trigger email notifications for orders marked as "invoiced" and not previously notified.
# automated action (ir.cron) to periodically check for invoiced sale orders and trigger the notification method.
# mail_template to format and send the email, including sale order details (number, total, status).
# invoiced_notification_sent field to the sale order form for tracking purposes.
# test emails are sent when sale orders reach the invoiced stage.
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoiced_notification_sent = fields.Boolean(string='Invoiced Notification Sent', default=False)

    @api.model
    def _compute_invoice_status(self):
        super(SaleOrder, self)._compute_invoice_status()

        for order in self:
            if order.invoice_status == 'invoiced' and not order.invoiced_notification_sent:
                # Send email notification
                mail_template = self.env.ref('test_sale_order_notifications.mail_template_sale_order_invoiced1')
                mail_template.send_mail(order.id, force_send=True)

                order.invoiced_notification_sent = True
                print(f"Notification sent for sale order: {order.name}")


    def send_invoiced_sale_order_notifications(self):
        print("inside")
        invoiced_orders = self.search(
            [('state', '=', 'sale'), ('invoice_status', '=', 'invoiced'), ('invoiced_notification_sent', '=', False)])

        for order in invoiced_orders:
            mail_template = self.env.ref('test_sale_order_notifications.mail_template_sale_order_invoiced1')
            mail_template.send_mail(order.id, force_send=True)
            print("true")
            order.invoiced_notification_sent = True
