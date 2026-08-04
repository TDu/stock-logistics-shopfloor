from odoo.addons.component.core import Component


class SinglePackTransfer(Component):
    _inherit = "shopfloor.single.pack.transfer"

    def _response_for_start(self, message=None, popup=None, jump_to_menu=False):
        if jump_to_menu:
            next_menu = self.work.menu._get_jumpto_menu(self)
            if next_menu:
                res = self._response_for_jump_to_menu(next_menu, message="Jumping!")
                return res
        return self._response(next_state="start", message=message, popup=popup)
