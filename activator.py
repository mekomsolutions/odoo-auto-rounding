import logging
import odoo
from odoo.exceptions import MissingError

_logger = logging.getLogger(__name__)

ROUND_UP_EXT_ID = "account_cash_rounding_1"


def on_startup(cr):
    _logger.info("Configuring auto rounding...")
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    rounding_field = env["ir.model.fields"].search([
        ("model", "=", "account.move"),
        ("name", "=", "invoice_cash_rounding_id")
    ])

    rounding_default = env["ir.default"].search([
        ("field_id", "=", rounding_field.id),
        ("user_id", "=", None)
    ])

    if not rounding_default or rounding_default.json_value == "0":
        #Existing implementations using the addon could have default set to 0 which is invalid, delete it.
        if rounding_default.json_value == "0":
            _logger.info("Removing invalid default rounding for method with id: %s", rounding_default.json_value)
            rounding_default.unlink()
            _logger.info("Successfully removed invalid default rounding")

        _logger.info("Looking up rounding method by external id: %s", ROUND_UP_EXT_ID)
        ext_id = env["ir.model.data"].search([
            ("model", "=", "account.cash.rounding"),
            ("module", "=", "init"),
            ("name", "=", ROUND_UP_EXT_ID)
        ])
        
        if ext_id.res_id != 0:
            rounding_method = env["account.cash.rounding"].search([("id", "=", ext_id.res_id)])
            _logger.info("Setting default rounding method to %s", rounding_method.name)
            env["ir.default"].create({
                "field_id": rounding_field.id,
                "json_value": ext_id.res_id
            })

            _logger.info("Successfully set default rounding method to %s", rounding_method.name)
        else:
            raise MissingError("No rounding method found matching external id: " + ROUND_UP_EXT_ID)
    else:
        default_method = env["account.cash.rounding"].search([("id", "=", rounding_default.json_value)])
        _logger.info("Default rounding method is already set to %s", default_method.name)
