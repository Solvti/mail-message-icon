from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, **kwargs):
        message = super(MailThread, self).message_post(**kwargs)
        if self._context.get("event_meeting"):
            event_id = self._context.get("event_meeting")
            if not isinstance(event_id, int):
                raise ValueError("event id must be integer!")
            event = self.env["calendar.event"].browse([event_id])
            if event.partner_ids:
                message.event_partner_ids = event.partner_ids.ids
            if event.event_message_error:
                message.event_message = event.event_message_error
            else:
                message.event_message = False
        if self._context.get("schedule_message"):
            mail_id = self._context.get("schedule_message")
            if not isinstance(mail_id, int):
                raise ValueError("scheduled mail_id must be integer!")
            message.mail_ids = [mail_id]
        return message
