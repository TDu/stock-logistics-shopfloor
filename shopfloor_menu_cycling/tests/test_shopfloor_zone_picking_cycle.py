# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import Command
from odoo.addons.shopfloor.tests.test_zone_picking_base import ZonePickingCommonCase


class ZonePickingCycleCase(ZonePickingCommonCase):

    def setUp(self):
        super().setUp()
        self.service.work.current_picking_type = self.picking1.picking_type_id
        self.service.work.menu.sudo().enable_menu_cycling = True
        self.menu2 = self.env.ref("shopfloor.shopfloor_menu_demo_single_pallet_transfer")

    def test_set_destination_location_cycle(self):
        """
        """
        self.service.work.menu.sudo().next_shopfloor_menu_ids = [Command.set(self.menu2.ids)]
        zone_location = self.zone_location
        picking_type = self.picking1.picking_type_id
        moves_before = self.picking1.move_ids
        # self.assertEqual(len(moves_before), 1)
        # self.assertEqual(len(moves_before.move_line_ids), 1)
        move_line = moves_before.move_line_ids
        response = self.service.dispatch(
            "set_destination",
            params={
                "move_line_id": move_line.id,
                "barcode": self.packing_location.barcode,
                "quantity": move_line.quantity,
                "confirmation": None,
            },
        )
        # Check response
        __import__("pdb").set_trace()
        self.assert_response(
            response,
            next_state="scan_location",
            data={}
            # data=dict(
            #     self._response_package_level_data(package_level),
            #     confirmation_required=None,
            # ),
        )
        return
        move_lines = self.service._find_location_move_lines()
        move_lines = move_lines.sorted(lambda x: x.move_id.priority, reverse=True)
        self.assert_response_select_line(
            response,
            zone_location,
            picking_type,
            move_lines,
            message=self.service.msg_store.confirm_pack_moved(),
        )

    def test_set_destination_location_no_cycle(self):
        """
        """
        zone_location = self.zone_location
        picking_type = self.picking1.picking_type_id
        moves_before = self.picking1.move_ids
        # self.assertEqual(len(moves_before), 1)
        # self.assertEqual(len(moves_before.move_line_ids), 1)
        move_line = moves_before.move_line_ids
        response = self.service.dispatch(
            "set_destination",
            params={
                "move_line_id": move_line.id,
                "barcode": self.packing_location.barcode,
                "quantity": move_line.quantity,
                "confirmation": None,
            },
        )
        # self.assertEqual(move_line.state, "done")
        # Check picking data
        # moves_after = self.picking1.move_ids
        # self.assertEqual(moves_before, moves_after)
        # self.assertEqual(move_line.qty_picked, 10)
        # Check response
        move_lines = self.service._find_location_move_lines()
        move_lines = move_lines.sorted(lambda x: x.move_id.priority, reverse=True)
        self.assert_response_select_line(
            response,
            zone_location,
            picking_type,
            move_lines,
            message=self.service.msg_store.confirm_pack_moved(),
        )
