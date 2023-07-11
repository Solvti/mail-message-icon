from odoo import models


class MailNotification(models.Model):
    _inherit = "mail.notification"

    def _notification_format(self):
        """
        Overridden.
        Add extra partner email.
        """
        notification_data_list = super(MailNotification, self)._notification_format()
        for notification_data in notification_data_list:
            if notification_data.get("res_partner_id"):
                notification_id = self.filtered(lambda n: n.id == notification_data.get("id"))
                notification_data["res_partner_id"].append(notification_id.res_partner_id.email)
        return notification_data_list
