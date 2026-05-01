# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import Command
from odoo.addons.shopfloor.tests.common import CommonCase

class ShopfloorMenuCycling(CommonCase):

    @classmethod
    def setUpClassVars(cls, *args, **kwargs):
        super().setUpClassVars(*args, **kwargs)
        cls.menu = cls.env.ref("shopfloor.shopfloor_menu_demo_zone_picking")
        cls.menu2 = cls.env.ref("shopfloor.shopfloor_menu_demo_location_content_transfer")

    def test_menu_cycling_not_configured(self):
        self.assertFalse(self.menu._get_next_menu())
        self.menu.sudo().enable_menu_cycling = True
        self.assertFalse(self.menu._get_next_menu())

    def test_menu_cycling_set_with_one_menu(self):
        self.menu.sudo().enable_menu_cycling = True
        self.menu.sudo().next_shopfloor_menu_ids = [Command.set([self.menu2.id])]
        self.assertEqual(self.menu._get_next_menu(), self.menu2)
