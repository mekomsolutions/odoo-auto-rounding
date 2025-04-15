import logging

from odoo import models

_logger = logging.getLogger(__name__)


class CustomAccountMove(models.Model):
    _inherit = "account.move"

    def _register_hook(self):
        rounding_field = self.env["ir.model.fields"].search([
            ("model", "=", "account.move"),
            ("name", "=", "invoice_cash_rounding_id")
        ])
        default_rounding_method = self.env["ir.default"].search([
            ("field_id", "=", rounding_field.id),
            ("user_id", "=", None)
        ])
        if not default_rounding_method:
            _logger.info("Setting default rounding method to up")
            ext_id = self.env["ir.model.data"].search([
                ("model", "=", "account.cash.rounding"),
                ("module", "=", "init"),
                ("name", "=", "account_cash_rounding_1")
            ])
            self.env["ir.default"].create({
                "field_id": rounding_field.id,
                "json_value": ext_id.res_id
            })
