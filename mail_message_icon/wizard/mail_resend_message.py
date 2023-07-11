from odoo import Command, api, fields, models


class MailResendMessage(models.TransientModel):
    _inherit = "mail.resend.message"

    @api.model
    def default_get(self, fields):
        """Overridden: Add status field for a resend message wizard."""
        message_id = self._context.get("mail_message_to_resend")
        mode = self._context.get("mail_status_mode", False)
        if not message_id or not mode:
            return super(MailResendMessage, self).default_get(fields)
        rec = super(models.TransientModel, self).default_get(fields)
        allow_resend = True if mode != "sent_status" else False
        mail_message_id = self.env["mail.message"].browse(message_id)
        notification_ids = mail_message_id.notification_ids.filtered(lambda notif: notif.notification_type == "email")
        partner_ids = [
            Command.create(
                {
                    "partner_id": notif.res_partner_id.id,
                    "name": notif.res_partner_id.name,
                    "email": notif.res_partner_id.email,
                    "resend": allow_resend,
                    "message": notif.failure_reason,
                    "status": notif.notification_status,
                }
            )
            for notif in notification_ids
        ]
        has_user = any(notif.res_partner_id.user_ids for notif in notification_ids)
        if has_user:
            partner_readonly = not self.env["res.users"].check_access_rights("write", raise_exception=False)
        else:
            partner_readonly = not self.env["res.partner"].check_access_rights("write", raise_exception=False)
        rec["partner_readonly"] = partner_readonly
        rec["notification_ids"] = [Command.set(notification_ids.ids)]
        rec["mail_message_id"] = mail_message_id.id
        rec["partner_ids"] = partner_ids
        return rec


class PartnerResend(models.TransientModel):
    _inherit = "mail.resend.partner"

    status = fields.Char(string="Status")
