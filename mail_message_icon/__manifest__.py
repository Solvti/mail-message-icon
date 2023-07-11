{
    "name": "Advanced Mail Icons in Chatter",
    "summary": "Additional mail icons, enabling faster identification of email statuses",
    "version": "16.0.1.0.0",
    "category": "Discuss",
    "author": "Solvti Sp. z o.o.",
    "website": "https://www.solvti.pl",
    "company": "Solvti",
    "maintainer": "Solvti",
    "license": "GPL-3",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": ["snailmail", "calendar"],
    "data": [
        "wizard/mail_resend_message_views.xml",
        "views/mail_message_views.xml",
    ],
    "assets": {
        "mail.assets_messaging": [
            "mail_message_icon/static/src/models/*.js",
        ],
        "web.assets_backend": [
            "mail_message_icon/static/src/components/advance_message_icon/thread_message_icon.xml",
            "mail_message_icon/static/src/components/message_notification_popover_content/message_notification_popover_content.xml",
        ],
    },
    "demo": [],
    "external_dependencies": {},
    "images": ["static/description/main.png"],
    "email": "support@solvti.pl",
}
