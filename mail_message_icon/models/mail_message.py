from odoo import fields, models


class Message(models.Model):
    _inherit = "mail.message"

    # TODO for refine, if needed to store attendance' partners or just Boolean Value is enough.
    event_partner_ids = fields.Many2many(
        "res.partner",
        "event_partner_ids_rel",
        string="Event Partners",
        help="Partners from event's attendees",
    )

    def _get_message_format_fields(self):
        fields_list = super(Message, self)._get_message_format_fields()
        return fields_list + ["event_partner_ids"]
