/** @odoo-module alias=mail_message_icon.advance_message_icon_message_view**/
import {attr} from "@mail/model/model_field";
import {clear} from "@mail/model/model_field_command";
import {markEventHandled} from "@mail/utils/utils";
import {registerPatch} from "@mail/model/model_core";

registerPatch({
    name: "MessageView",
    recordMethods: {
        /**
         * @override
         * @param {MouseEvent} ev
         */
        onClickFailure(ev) {
            if (this.message && this.message.message_type !== "snailmail") {
                markEventHandled(ev, "Message.ClickFailure");
                this.message.openResendAction(this.message.mailStatus);
            } else {
                this._super(...arguments);
            }
        },
    },

    fields: {
        /**
         * @override
         */
        notificationIconNewClassName: attr({
            compute() {
                if (this.message.mailStatus === "failure_status") {
                    return "fa fa-envelope text-danger";
                } else if (this.message.mailStatus === "sent_status") {
                    return "fa fa-envelope text-success";
                } else if (this.message.mailStatus === "bounce_status") {
                    return "fa fa-envelope text-warning";
                } else if (this.message.mailStatus === "ready_status") {
                    return "fa fa-envelope text-primary";
                } else if (this.message.mailStatus === "canceled_status") {
                    return "fa fa-envelope text-mutes opacity-50";
                }
                return clear();
            },
            default: "fa fa-envelope",
        }),
    },
});
