/**
 * Copyright 2026 Camptocamp SA (http://www.camptocamp.com)
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

import {process_registry} from "/shopfloor_mobile_base/static/src/services/process_registry.esm.js";

const reception_scenario = process_registry.get("reception");
const _get_states = reception_scenario.component.methods._get_states;
// // Get the original template of the reception scenario
const template = reception_scenario.component.template;
// // And inject the new state template (for this module) into it
const position_string = "<!-- measuring-device-placeholder -->"
const pos = template.indexOf(position_string);
const new_template_prov =
    template.replace(position_string,
    `
        <v-row>
            <v-col class="text-center" cols="12">
                <btn-action @click="state.use_measuring_device">BANG - BANG</btn-action>
            </v-col>
        </v-row>
    `
    )
const pos2= new_template_prov.indexOf("</Screen>");
const new_template =
    new_template_prov.substring(0, pos2)
    +
    `
 <div v-if="state_is('use_measuring_device')">

    <separator-title>Go to the measuring device then confirm with ok.</separator-title>

     <div class="button-list button-vertical-list full">
         <v-row align="center">
             <v-col class="text-center" cols="12">
                 <btn-action @click="state.on_ok">OK</btn-action>
             </v-col>
         </v-row>
     </div>

 </div>

    ` +
    new_template_prov.substring(pos2);

// // Extend the reception scenario with :
// //   - the new patched template
// //   - the js code for the new state
const ReceptionMeasuringDevice = process_registry.extend("reception", {
    template: new_template,
//     "methods.get_packaging_measurements": function () {
//         return ["length", "width", "height", "weight", "qty", "barcode"];
//     },
    "methods._get_states": function () {
        const states = _get_states.bind(this)();
        states.use_measuring_device = {
            display_info: {
                title: "Using measuring device",
            },
            on_ok: () => {
                this.wait_call(
                    this.odoo.call("set_packaging_dimension__measuring_device_release", {
                        picking_id: this.state.data.picking.id,
                        selected_line_id: this.state.data.selected_move_line.id,
                        packaging_id: this.state.data.packaging.id,
                    })
                );
            },
        };
        return states;
    },
});

process_registry.replace("reception", ReceptionMeasuringDevice);
