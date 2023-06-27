import pytz
from odoo import _, api, models


class Meeting(models.Model):
    _inherit = "calendar.event"

    @api.model
    def create(self, values):
        """Whenever new event is created with applicant, create message with confirmation in applicant's chatter."""
        meeting = super(Meeting, self).create(values)
        if meeting.applicant_id:
            timezone = self._context.get("tz") or self.env.user.partner_id.tz or "UTC"
            meeting.applicant_id.with_context(create_note_from_event_id=meeting.id).message_post(
                body=_(
                    "New meeting is created:<br />"
                    "Date: <b>%s</b>,<br />"
                    "Subject: <b>%s</b>,<br />"
                    "Attendees: <b>%s</b>,<br />"
                    "%s"
                )
                % (
                    meeting.start.astimezone(pytz.timezone(timezone)).strftime("%d.%m.%Y %H:%M"),
                    meeting.display_name,
                    "; ".join([str(partner.email) for partner in meeting.partner_ids]),
                    meeting.description,
                )
            )
        return meeting

    def write(self, vals):
        """
        Update meeting message whenever start date changed.
        create message with confirmation in applicant's chatter.
        """
        result = super(Meeting, self).write(vals)
        if "start" in vals and isinstance(vals["start"], str):
            for rec in self:
                if rec.applicant_id:
                    timezone = self._context.get("tz") or self.env.user.partner_id.tz or "UTC"
                    rec.applicant_id.with_context(create_note_from_event_id=self.id).message_post(
                        body=_(
                            "Meeting date has changed:<br />"
                            "Date: <b>%s</b>,<br />"
                            "Subject: <b>%s</b>,<br />"
                            "Attendees: <b>%s</b>,<br />"
                            "%s"
                        )
                        % (
                            rec.start.astimezone(pytz.timezone(timezone)).strftime("%d.%m.%Y %H:%M"),
                            rec.display_name,
                            "; ".join([str(partner.email) for partner in self.partner_ids]),
                            rec.description,
                        )
                    )
        return result
