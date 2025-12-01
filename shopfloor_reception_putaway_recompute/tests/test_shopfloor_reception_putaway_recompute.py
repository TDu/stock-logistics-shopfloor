# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.shopfloor_reception.tests.common import CommonCase

class TestShopfloorReceptionPutawayRecompute(CommonCase):
    @classmethod
    def setUpClassBaseData(cls):
        super().setUpClassBaseData()

    def test_recompute_putaway(self):
        picking = self._create_picking(
            lines=[(self.product_a, 10), (self.product_b, 5)]
        )
