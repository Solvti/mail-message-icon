odoo.define("mail_message.mail_message_icon", function (require) {
    "use strict";

    var core = require("web.core");
    var QWeb = core.qweb;
    var ThreadWidget = require("mail.widget.Thread");
    var Message = require("mail.model.Message");

    Message.include({
        _setInitialData: function (data) {
            this._super.apply(this, arguments);
            this._mail_ids = data.mail_ids || [];
            this._EmailStatus = data.email_status;
        },
        hasEmailData: function () {
            return Boolean(this._mail_ids && this._mail_ids.length > 0);
        },
        getEmailStatus: function () {
            if (!this.hasEmailData()) {
                return undefined;
            }
            return this._EmailStatus;
        },
        getEmailData: function () {
            if (!this.hasEmailData()) {
                return undefined;
            }
            return this._mail_ids;
        },
    });

    ThreadWidget.include({
        render: function (thread, options) {
            var self = this._super.apply(this, arguments);
            var messages = _.clone(thread.getMessages({domain: options.domain || []}));
            this._renderMessageEMailPopover(messages);
            return self;
        },
        _renderMessageEMailPopover: function (messages) {
            if (this._messageMailPopover) {
                this._messageMailPopover.popover("hide");
            }
            if (!this.$(".o_thread_email_tooltip").length) {
                return;
            }
            this._messageMailPopover = this.$(".o_thread_email_tooltip").popover({
                html: true,
                boundary: "viewport",
                placement: "top",
                trigger: "hover",
                offset: "0, 1",
                content: function () {
                    var messageID = $(this).data("message-id");
                    var ShowMessage = _.find(messages, function (message) {
                        return message.getID() === messageID;
                    });
                    return QWeb.render("mail.widget.Thread.Message.MailTooltip.email", {
                        data: ShowMessage.hasEmailData()
                            ? ShowMessage.getEmailData()
                            : [],
                    });
                },
            });
        },
    });
});
