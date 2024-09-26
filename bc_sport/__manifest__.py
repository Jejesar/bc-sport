{
    "name": "BC Sport",
    "version": "0.1",
    "category": "Games",
    "summary": """
        BC Sport is a module that allows you to manage sports competitions.
    """,
    "description": """
        BC Sport is a module that allows you to manage sports competitions.
        - Ping-pong
    """,
    "author": "Jérôme SARTIAUX",
    "website": "https://jejesar.be",
    "depends": ["base", "mail", "web", "contacts", "website"],
    "data": [
        # MENUS
        "views/menu.xml",
        # VIEWS
        "views/match.xml",
        "views/player.xml",
        "views/res_partner.xml",
        # TEMPLATES
        "templates/website_matches.xml",
        # SECURITY
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.assets_frontend": ["bc_sport/static/src/**/*"],
        "web.assets_backend": [
            "bc_sport/static/src/components/**/*.js",
            "bc_sport/static/src/components/**/*.xml",
            "bc_sport/static/src/components/**/*.scss",
        ],
    },
    "license": "LGPL-3",
    "application": True,
}
