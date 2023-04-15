{
    "name": "Mail Message Icon",
    "summary": "Better overview over sent messages in chatter.",
    "version": "13.0.1.0.1",
    "category": "Mail",
    "author": "Solvti Sp. z o.o.",
    "license": "GPL-3",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": ["mail", "calendar"],
    "data": [
        "views/assets.xml",
        "views/mail_message_view.xml",
    ],
    "qweb": ["static/src/xml/mail_message_icon.xml"],
    "demo": [],
    "external_dependencies": {},
}
