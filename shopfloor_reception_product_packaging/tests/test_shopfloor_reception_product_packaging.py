# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.shopfloor_reception.tests.common import CommonCase


# pylint: disable=W8110
class TestShopfloorReceptionProductPackaging(CommonCase):
    @classmethod
    def setUpClassBaseData(cls):
        super().setUpClassBaseData()
        cls.picking = cls._create_picking(
            lines=[(cls.product_a, 10), (cls.product_b, 10), (cls.product_c, 10)]
        )
        # Picking has 3 products
        # Product A with one packaging of quantity 3
        # Product B with no packaging
        cls.product_b.packaging_ids = [(5, 0, 0)]
        # Product C with 2 packaging
        # cls.product_c_packaging_2 = (
        #     cls.env["product.packaging"]
        #     .sudo()
        #     .create(
        #         {
        #             "name": "Big Box",
        #             "product_id": cls.product_c.id,
        #             "barcode": "ProductCBigBox",
        #             "qty": 6,
        #         }
        #     )
        # )

    def test_process_with_new_pack__package_type_is_set(self):
        picking = self.picking
        self.service.dispatch("scan_document", params={"barcode": picking.name})
        selected_move_line = picking.move_line_ids.filtered(
            lambda li: li.product_id == self.product_a
        )
        self.assertEqual(len(selected_move_line), 1)
        response = self.service.dispatch(
            "process_with_new_pack",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
                "quantity": 3.0,
            },
        )
        picking_data = self.data.picking(picking)
        self.assert_response(
            response,
            next_state="set_destination",
            data={
                "picking": picking_data,
                "selected_move_line": self.data.move_lines(selected_move_line),
            },
        )
        package = selected_move_line.result_package_id
        self.assertTrue(package.product_packaging_id)

    def test_process_with_new_pack__package_type_not_set(self):
        picking = self.picking
        self.service.dispatch("scan_document", params={"barcode": picking.name})
        selected_move_line = picking.move_line_ids.filtered(
            lambda li: li.product_id == self.product_a
        )
        self.assertEqual(len(selected_move_line), 1)
        response = self.service.dispatch(
            "process_with_new_pack",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
                "quantity": 5.0,
            },
        )
        picking_data = self.data.picking(picking)
        self.assert_response(
            response,
            next_state="set_destination",
            data={
                "picking": picking_data,
                "selected_move_line": self.data.move_lines(selected_move_line),
            },
        )
        package = selected_move_line.result_package_id
        self.assertFalse(package.product_packaging_id)

    def test_scan_new_package__package_type_set(self):
        picking = self.picking
        selected_move_line = picking.move_line_ids.filtered(
            lambda li: li.product_id == self.product_a
        )
        selected_move_line.qty_picked = 3
        response = self.service.dispatch(
            "select_dest_package",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
                "barcode": "FooBar",
                "confirmation": True,
            },
        )
        self.assertEqual(response.get("next_state"), "select_move")
        package = selected_move_line.result_package_id
        self.assertEqual(package.name, "FooBar")
        self.assertTrue(package.product_packaging_id)
