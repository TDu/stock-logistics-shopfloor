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
        # cls.package_type = cls.env["stock.package.type"]
        cls.package_type = cls.env.ref("stock.package_type_01")
        cls.package_type.sudo().barcode = "CAGE"
        product_a_packaging = cls.product_a.packaging_ids
        product_a_packaging.package_type_id = cls.package_type
        cls.storage_types = cls.env["stock.package.type"].search([("package_carrier_type", "=", "none")])

    def test_go_to_set_storage_type_screen(self):
        picking = self.picking
        self.service.dispatch("scan_document", params={"barcode": picking.name})
        selected_move_line = picking.move_line_ids.filtered(
            lambda li: li.product_id == self.product_a
        )
        self.assertEqual(len(selected_move_line), 1)
        response = self.service.dispatch(
            "set_storage_type",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
            },
        )
        # FIXME
        response["data"]["set_storage_type"]["picking"].pop("progress")
        self.assert_response(
            response,
            next_state="set_storage_type",
            data={
                "picking": self.data.picking(picking),
                "selected_move_line": self.data.move_lines(selected_move_line),
                "storage_types": [ self.data.delivery_packaging(pack) for pack in self.storage_types],
            },
        )

    def test_change_storage_type_on_package(self):
        picking = self.picking
        self.service.dispatch("scan_document", params={"barcode": picking.name})
        selected_move_line = picking.move_line_ids.filtered(
            lambda li: li.product_id == self.product_a
        )
        selected_move_line.qty_picked = selected_move_line.quantity_product_uom

        response = self.service.dispatch(
            "select_dest_package",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
                "barcode": "CAGE-0001",
                "confirmation": True,
            },
        )

        # self.assertEqual(len(selected_move_line), 1)
        response = self.service.dispatch(
            "set_storage_type",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
                "barcode": "CAGE",
            },
        )
        # response["data"]["set_storage_type"]["picking"].pop("progress")
        self.assertEqual(response["next_state"], "set_destination")
        self.assertTrue(selected_move_line.result_package_id)
        self.assertEqual(selected_move_line.result_package_id.package_type_id, self.package_type)
        # self.assert_response(
        #     response,
        #     next_state="set_destination",
        #     data={
        #         "picking": self.data.picking(picking),
        #         "selected_move_line": self.data.move_lines(selected_move_line),
        #     },
        # )
