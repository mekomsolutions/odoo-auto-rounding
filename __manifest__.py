{
    "name": "Auto Rounding",
    "version": "14.0.0.0.0",
    "license": "AGPL-3",
    "author": (
        "Mekom Solutions"
    ),
    "website": "https://github.com/mekomsolutions/odoo-auto-rounding",
    "summary": "Configures the default rounding method on invoices",
    "depends": ["account", "odoo_initializer"],
    "data": [],
    "demo": [],
    "installable": True,
    "auto_install": True,
    "post_startup_hook": 'on_startup'
}
