from odoo import fields, models


class Meeting(models.Model):
    _inherit = "calendar.event"

    event_message_error = fields.Char(
        "Event Message error", help="Field that save information about error messages"
    )
