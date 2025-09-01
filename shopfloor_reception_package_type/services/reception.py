# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component


class Reception(Component):
    _inherit = "shopfloor.reception"

    def set_storage_type(self, picking_id, selected_line_id, barcode=""):
        """ """
        picking = self.env["stock.picking"].browse(picking_id)
        selected_line = self.env["stock.move.line"].browse(selected_line_id)
        message = self._check_picking_processible(picking)
        if message:
            return self._response_for_select_dest_package(
                picking, selected_line, message=message
            )
        if not selected_line.exists():
            message = self.msg_store.record_not_found()
            return self._response_for_select_dest_package(
                picking, selected_line, message=message
            )
        if barcode:
            storage_type = self.env["stock.package.type"].search([("barcode", "=", barcode)])
            if not storage_type.exists():
                message = self.msg_store.package_type_not_found()
            else:
                selected_line.result_package_id.package_type_id = storage_type
                message = self.msg_store.package_type_changed()
                return self._response_for_set_destination(picking, selected_line, message=message)
        return self._response_for_set_storage_type(picking, selected_line, message=message)

    def _get_storage_type(self, line):
        domain = [("package_carrier_type", "=", "none"), ("barcode", "!=", False)]
        return self.env["stock.package.type"].search(domain)

    def _response_for_set_storage_type(self, picking, line, message=None):
        storage_types = self._get_storage_type(line)
        data = {
            "selected_move_line": self._data_for_move_lines(line),
            "picking": self._data_for_stock_picking(picking, with_lines=False),
            "storage_types": self._data_for_storage_types(storage_types),
        }
        return self._response(
            next_state="set_storage_type", data=data, message=message
        )

    def _data_for_storage_type(self, storage_type):
        return self.data.delivery_packaging(storage_type)

    def _data_for_storage_types(self, storage_types):
        return [
            self._data_for_storage_type(storage_type)
            for storage_type in storage_types
        ]

class ShopfloorReceptionValidator(Component):
    _inherit = "shopfloor.reception.validator"

    def set_storage_type(self):
        return {
            "picking_id": {"coerce": to_int, "required": True, "type": "integer"},
            "selected_line_id": {
                "coerce": to_int,
                "type": "integer",
                "required": True,
            },
            "barcode": {"type": "string", "required": False},
        }
