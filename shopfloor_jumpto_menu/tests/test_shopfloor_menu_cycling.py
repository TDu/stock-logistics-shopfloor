# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.shopfloor.tests.common import CommonCase


class ShopfloorJumpToMenu(CommonCase):
    @classmethod
    def setUpClassVars(cls, *args, **kwargs):
        super().setUpClassVars(*args, **kwargs)
        cls.menu = cls.env.ref("shopfloor.shopfloor_menu_demo_zone_picking")
        cls.menu2 = cls.env.ref(
            "shopfloor.shopfloor_menu_demo_location_content_transfer"
        )

    def test_jump_to_menu_enabling(self):
        self.assertFalse(self.menu._get_jumpto_menu())
        self.menu.sudo().jump_to_menu_id = self.menu2
        self.assertTrue(self.menu._get_jumpto_menu())
