# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.component.core import Component


class ZonePicking(Component):
    _inherit = "shopfloor.zone.picking"

    def _process_next_line(self, message=None):
        jump_to_menu = self.work.menu._get_jumpto_menu(self)
        if jump_to_menu:
            res = self._response_for_jump_to_menu(jump_to_menu, message="Jumping!")
            return res
        return super()._process_next_line(message=message)
