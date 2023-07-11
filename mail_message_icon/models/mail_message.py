from odoo import fields, models


class Message(models.Model):
    _inherit = "mail.message"

    event_partner_ids = fields.Many2many(
        "res.partner",
        "event_partner_ids_rel",
        string="Event Partners",
        help="Store Partners from event's attendees when creating a note from event.",
    )

    def _get_message_format_fields(self):
        """
        Overridden.
        Add extra event_partner_ids to show Calendar Icon in message note chatter.
        """
        fields_list = super(Message, self)._get_message_format_fields()
        return fields_list + ["event_partner_ids"]
