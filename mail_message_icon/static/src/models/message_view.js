/** @odoo-module alias=mail_message_icon.advance_message_icon_message_view**/
import { registerPatch } from '@mail/model/model_core';
import { attr} from '@mail/model/model_field';
import { clear } from '@mail/model/model_field_command';

registerPatch({
    name: 'MessageView',
    recordMethods: {
        /**
         * @override
         */
        onClickNotificationIcon() {
            if (this.message && this.message.message_type !== 'snailmail') {
                this.message.openResendAction(true);
            }
            else {
              return this._super();
            }
        }
        
    },
    fields: {
        /**
         * @override
         */
        notificationIconNewClassName: attr({
            compute() {
                if (this.message.mailStatus === 'failure_status'){
                    return 'fa fa-envelope text-danger';
                }
                else if (this.message.mailStatus === 'sent_status'){
                    return 'fa fa-envelope text-success';
                }
                else if (this.message.mailStatus === 'bounce_status'){
                    return 'fa fa-envelope text-warning';
                }
                else if (this.message.mailStatus === 'ready_status'){
                    return 'fa fa-envelope text-primary';
                }

                
                return clear();
            },
            default: 'fa fa-envelope',
        }),
    }
});