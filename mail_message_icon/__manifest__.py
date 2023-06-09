{
    "name": "Advanced Mail Icons in Chatter",
    "summary": "Additional mail icons, enabling faster identification of email statuses",
    "version": "13.0.1.0.1",
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
        "views/assets.xml",
        "views/mail_message_view.xml",
    ],
    "qweb": ["static/src/xml/mail_message_icon.xml"],
    "demo": [],
    "external_dependencies": {},
    "images": ["static/description/main.png"],
    "email": "support@solvti.pl",
}
