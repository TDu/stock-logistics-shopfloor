# Copyright 2026 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

class ShopfloorMenu(models.Model):
    _inherit = "shopfloor.menu"

    enable_menu_cycling = fields.Boolean()
    next_shopfloor_menu_ids = fields.Many2many(
        comodel_name="shopfloor.menu",
        relation="shopfloor_menu_cycling",
        column1="menu_id",
        column2="next_menu_id",
        string="Next shopfloor menu", help="Possible menu to do at the end of the current one"
    )

    def _get_next_menu(self, params=None):
        """Return the next menu to do after the current one."""
        self.ensure_one()
        next_menus = self.next_shopfloor_menu_ids
        if not self.enable_menu_cycling or not next_menus:
            return False
        # If there are several possible next menus, how to choose
        # TODO filter the ones with operations to do
        return fields.first(next_menus)
        # __import__("pdb").set_trace()
        # with self.work_on(self._name) as work:
            # self.mm = work.component(usage=.scenario_id.key)
