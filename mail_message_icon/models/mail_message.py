from odoo import api, fields, models


class Message(models.Model):
    _inherit = "mail.message"

    event_partner_ids = fields.Many2many(
        "res.partner",
        "event_partner_ids_rel",
        string="Event Partners",
        help="Partner ids from event's attendees",
    )
    event_message = fields.Char(help="Field that store information about event's status")

    @api.model
    def _message_read_dict_postprocess(self, messages, message_tree):
        """Override the method to add extra information regarding email delivery status, visible in chatter.
        ref: addons/mail/models/mail_message.py
        """
        res = super(Message, self)._message_read_dict_postprocess(messages, message_tree)
        # Update dict of message with mail_ids or event message
        for message_dict in messages:
            message_id = message_dict.get("id")
            message = message_tree[message_id]
            mails_status = ""
            email_data = []
            bounced_partners = {}

            # handle mail_ids to show email icon
            if message.mail_ids:
                mails_status = message._get_mails_status()
                if mails_status == "bounce":
                    # When Bounce, Take which notification partners were bounced
                    for notif in message.notification_ids:
                        if notif.notification_status == "bounce":
                            bounced_partners[notif.res_partner_id.id] = notif.res_partner_id.email
                for mail in message.mail_ids:
                    state = mail.state
                    comment = mail.failure_reason if mail.failure_reason else ""
                    data = self.env["mail.message"]._get_email_data(
                        mail, state, comment, bounced_partners, mails_status
                    )
                    email_data = email_data + data
            # handle event message to show calendar icon
            elif message.event_partner_ids:
                partners = self.env["res.partner"].sudo()
                mails_status = "calendar" if not message.event_message else "exception_calendar"
                partners = message.event_partner_ids
                for partner in partners:
                    email_data.append(
                        (
                            partner.id,
                            partner.name,
                            partner.email,
                            "calendar",
                            message.event_message,
                        )
                    )
            message_dict.update(
                {
                    "email_status": mails_status,
                    "mail_ids": email_data,
                }
            )
        return res

    def _get_mails_status(self):
        """Return "general Message status"
        Depends on all sent Mails
        """
        self.ensure_one()
        mails_status = (
            (all(n.state == "sent" for n in self.mail_ids) and "sent")
            or (any(n.state == "exception" for n in self.mail_ids) and "exception")
            or (any(n.state == "outgoing" for n in self.mail_ids) and "outgoing")
            or "ready"
        )
        # Check if bounced
        if mails_status == "sent" and any(
            n.notification_status == "bounce" for n in self.notification_ids if n.notification_type == "email"
        ):
            mails_status = "bounce"
        return mails_status

    @api.model
    def _get_email_data(self, mail, state, comment, bounced_partners, mails_status):
        """Prepare and return emails data
        - if there are recipient_ids, return list with each recipient's data
        - if email_to is present, returns the list of those email addresses.
        """
        email_list = []
        if mail.recipient_ids:
            for partner in mail.recipient_ids:
                # Update state and comment when bounced email
                if bounced_partners.get(partner.id, False):
                    state = "bounce"
                    comment = f"Your message to {partner.email} couldn't be delivered."
                email_list.append(
                    (
                        partner.id,
                        partner.name,
                        partner.email,
                        state,
                        comment,
                    )
                )
        elif mail.email_to:
            # Update state and comment if bounced email
            if mails_status == "bounce" and mail.notification_ids:
                for notif in mail.notification_ids:
                    if notif.res_partner_id and bounced_partners.get(notif.res_partner_id.id, False):
                        state = "bounce"
                        comment = f"Your message to {notif.res_partner_id.email} couldn't be delivered."
            # It's possible to have many emails in email_to field. Show them all.
            emails = mail.email_to.split(",")
            for email in emails:
                email_list.append(
                    (
                        [],
                        email,
                        email,
                        state,
                        comment,
                    )
                )
        return email_list
