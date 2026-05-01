# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.component.core import Component


class ZonePicking(Component):
    _inherit = "shopfloor.zone.picking"

    def _process_next_line(self, message=None):
        # TODO check if we have a possible cycle menu
        next_menu = self.work.menu._get_next_menu(self)
        if next_menu:
            service = self.component(next_menu.scenario_id.key)
            service.work.menu = next_menu
            # return service.start(barcode="")
            return service._response_for_start()
        return super()._process_next_line(message=message)

# Try to hack the validation, but too messy
# We will send the data to the front-end and he will call the endpoint

# class ShopfloorZonePickingValidatorResponse(Component):
#     _inherit = "shopfloor.zone_picking.validator.response"

#     def _states(self):
#         res = super()._states()
#         validator = self.component("single_pack_transfer.validator.response")
#         # schema_for_scan_location = validator._schema_for_package_level_details(required=True)
#         # schema_for_scan_location.update(validator._schema_confirmation_required())
#         # res["set_destination"] = schema_for_scan_location
#         schema_for_start = self._schema_for_package_level_details()
#         schema_for_start.update(self._schema_confirmation_required())
#         res["start"] = schema_for_start
#         return res


