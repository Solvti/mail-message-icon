/** @odoo-module alias=mail_message_icon.advance_message_icon_notification **/
import {insert} from "@mail/model/model_field_command";
import {registerPatch} from "@mail/model/model_core";

registerPatch({
    name: "Notification",
    modelMethods: {
        /**
         * @override
         * Add extra partner email information to partner data in order to show it when clicking Message Icon.
         * @param {Object} data
         * @returns {Object}
         */
        convertData(data) {
            const data2 = this._super(data);
            if ("res_partner_id" in data && data.res_partner_id.length === 3 && data2.partner._value.id) {
                data2.partner = insert({
                    email: data.res_partner_id[2],
                    display_name: data.res_partner_id[1],
                    id: data.res_partner_id[0],
                });
            }
            return data2;
        },
    },
});
