# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


from odoo.addons.component.core import Component


class Reception(Component):
    _inherit = "shopfloor.reception"

    # # TODO could also be done in _put_in_pack with a context key
    # def process_with_new_pack(self, picking_id, selected_line_id, quantity):
    #     res = super().process_with_new_pack(picking_id, selected_line_id, quantity)
    #     if res.get("next_state", "") == "set_destination":
    #         line = self.env["stock.move.line"].browse(selected_line_id)
    #         package = line.result_package_id
    #         if package:
    #             # Should this be done before generating the response ?
    #             packaging = package._search_product_packaging(line.product_id, line.qty_picked)
    #             package.product_packaging_id = packaging
    #     return res

    # def _set_package_on_move_line(self, picking, line, package):
    #     res = super()._set_package_on_move_line( picking, line, package)
    #     if res is None and line.result_package_id:
    #         packaging = package._search_product_packaging(line.product_id, line.qty_picked)
    #         package.product_packaging_id = packaging
    #     return res

    # def _package_assign_product_packaging(self, product_id, quantity):
    #     ...
