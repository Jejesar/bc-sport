/** @odoo-module */

import { Component, onWillStart } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class Leaderboard extends Component {
    static template = "bc_sport.Leaderboard";

    setup() {
        async () => {
            await loadJS(
                "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.min.js"
            );
        };
        this.orm = useService("orm");

        this.players = [];
        onWillStart(async () => {
            this.players = await this.orm.searchRead("bc_sport.player", [], []);

            console.log(this.players);
        });
    }
}

registry.category("actions").add("bc_sport.leaderboard", Leaderboard);
