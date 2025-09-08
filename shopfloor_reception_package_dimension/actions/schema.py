# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.component.core import Component


class ShopfloorSchemaAction(Component):
    _inherit = "shopfloor.schema.action"

    def package(self, with_packaging=False):
        res = super().package(with_packaging=with_packaging)
        res["height"] = {"type": "float", "nullable": True, "required": False}
        res["height_uom"] = {"type": "string", "nullable": True, "required": False}
        return res
