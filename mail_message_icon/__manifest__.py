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
    "depends": ["mail", "calendar"],
    "data": [
        "views/mail_message_views.xml",
    ],
    "qweb": ["static/src/xml/mail_message_icon.xml"],
    'assets': {
        'web.assets_backend': [
            'mail_message_icon/static/src/components/advance_message_icon/mail_message_icon.js',
            'mail_message_icon/static/src/components/advance_message_icon/thread_message_icon.xml',
        ],
        'web.assets_common': [
            'mail_message_icon/static/src/components/advance_message_icon/style.css',
        ],
    },
    "demo": [],
    "external_dependencies": {},
    "images": ["static/description/main.png"],
    "email": "support@solvti.pl",
}
