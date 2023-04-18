import pytz

from odoo import _, api, models


class Meeting(models.Model):
    _inherit = "calendar.event"

    @api.model
    def create(self, values):
        """Whenever new event is created with applicant, create message with confirmation in applicant's chatter."""
        meeting = super(Meeting, self).create(values)
        if meeting.applicant_id:
            timezone = pytz.timezone(
                self.env.context["tz"] if "tz" in self.env.context and self.env.context["tz"] else "utc"
            )
            meeting.applicant_id.with_context(message_calendar_event_id=meeting.id).message_post(
                body=_(
                    "New meeting is created:<br />"
                    "Date: <b>%s</b>,<br />"
                    "Subject: <b>%s</b>,<br />"
                    "Attendees: <b>%s</b>,<br />"
                    "%s"
                )
                % (
                    meeting.start.astimezone(timezone).strftime("%d.%m.%Y %H:%M"),
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
        if "start" in vals and isinstance(vals["start"], str) and self.applicant_id:
            timezone = pytz.timezone(
                self.env.context["tz"] if "tz" in self.env.context and self.env.context["tz"] else "utc"
            )
            self.applicant_id.with_context(message_calendar_event_id=self.id).message_post(
                body=_(
                    "Meeting date has changed:<br />"
                    "Date: <b>%s</b>,<br />"
                    "Subject: <b>%s</b>,<br />"
                    "Attendees: <b>%s</b>,<br />"
                    "%s"
                )
                % (
                    self.start.astimezone(timezone).strftime("%d.%m.%Y %H:%M"),
                    self.display_name,
                    "; ".join([str(partner.email) for partner in self.partner_ids]),
                    self.description,
                )
            )
        return result
