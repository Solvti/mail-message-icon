/** @odoo-module alias=mail_message_icon.advance_message_icon_message **/
import { registerPatch } from '@mail/model/model_core';
import { attr} from '@mail/model/model_field';

registerPatch({
    name: 'Message',
    recordMethods: {
        /**
         * @override
         */
        openResendAction(all = false) {
            console.log("2");
            if (this.message_type !== 'sms' && all === true) {
                console.log("3");
                this.env.services.action.doAction(
                    'mail_message_icon.mail_message_send_status_action',
                    {
                        additionalContext: {
                            mail_message_to_resend: this.id,
                            show_all_mails: true,
                        },
                    }
                );
            } else {
                this._super(...arguments);
            }
        },
    },
    fields: {
        mailStatus: attr({
            compute() {
                var sent = this.notifications.filter(notifications => notifications.notification_status === "sent");
                if (sent.length === this.notifications.length){
                    return "sent_status";
                }
                var exception = this.notifications.filter(notifications => notifications.notification_status === "exception");
                if (exception.length > 0){
                    return "failure_status";
                }
                var bounce = this.notifications.filter(notifications => notifications.notification_status === "bounce");
                if (bounce.length > 0){
                    return "bounce_status";
                }
                var ready = this.notifications.filter(notifications => notifications.notification_status === "ready");
                if (ready.length > 0){
                    return "ready_status";
                }
                return ""
            },
        }),
    }
});
