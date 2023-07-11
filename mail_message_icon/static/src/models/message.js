/** @odoo-module alias=mail_message_icon.advance_message_icon_message **/
import {attr} from "@mail/model/model_field";
import {registerPatch} from "@mail/model/model_core";

registerPatch({
    name: "Message",
    modelMethods: {
        /**
         * @override
         */
        convertData(data) {
            const data2 = this._super(data);
            if ("event_partner_ids" in data && data.event_partner_ids.length > 0 && "is_note" in data && data.is_note === true) {
                data2.calendarEventNote = true;
            }
            return data2;
        },
    },

    recordMethods: {
        /**
         * @override
         */
        openResendAction(mode = "") {
            if (this.message_type !== "sms" && mode !== "") {
                this.env.services.action.doAction("mail.mail_resend_message_action", {
                    additionalContext: {
                        mail_message_to_resend: this.id,
                        mail_status_mode: mode,
                    },
                });
            } else {
                this._super(...arguments);
            }
        },
    },
    fields: {
        mailStatus: attr({
            compute() {
                var canceled = this.notifications.filter((notifications) => notifications.notification_status === "canceled");
                // All Mails have status canceled -> set canceled status
                if (canceled.length === this.notifications.length) {
                    return "canceled_status";
                }
                var sent = this.notifications.filter((notifications) => notifications.notification_status === "sent");
                // If some mails have status canceled and sent only, set status as sent_status.
                if (canceled.length + sent.length === this.notifications.length) {
                    return "sent_status";
                }
                var exception = this.notifications.filter((notifications) => notifications.notification_status === "exception");
                if (exception.length > 0) {
                    return "failure_status";
                }
                var bounce = this.notifications.filter((notifications) => notifications.notification_status === "bounce");
                if (bounce.length > 0) {
                    return "bounce_status";
                }
                var ready = this.notifications.filter((notifications) => notifications.notification_status === "ready");
                if (ready.length > 0) {
                    return "ready_status";
                }
                if (canceled.length > 0) {
                    return "canceled_status";
                }
                return "";
            },
        }),
        calendarEventNote: attr({
            default: false,
        }),
    },
});
