from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, **kwargs):
        """Overridden:
        Add extra information whenever creating a new message note from calendar.event
        to be able to show attendance of event.
        """
        message = super(MailThread, self).message_post(**kwargs)
        if event_id := self._context.get("create_note_from_event_id"):
            if not isinstance(event_id, int):
                raise ValueError("Calendar event id must be integer!")
            event = self.env["calendar.event"].browse([event_id])
            if event.partner_ids:
                message.event_partner_ids = event.partner_ids.ids
        return message
