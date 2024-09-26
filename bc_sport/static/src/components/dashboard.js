/** @odoo-module */

import { Component, onWillStart } from "@odoo/owl";
import { loadJS, loadCSS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class Dashboard extends Component {
    static template = "bc_sport.Dashboard";

    setup() {
        async () => {
            await loadJS(
                "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.min.js"
            );
            await loadCSS(
                "https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"
            );
        };
        this.orm = useService("orm");
        this.action = useService("action");

        this.players = [];
        onWillStart(async () => {
            this.players = await this.orm.search("bc_sport.player", []);
            this.players_count = this.players.length;

            this.matches = await this.orm.search("bc_sport.match", []);
            this.matches_count = this.matches.length;
        });
    }

    async onClickPlayers() {
        try {
            await this.action.doAction("bc_sport.action_bc_sport_players");
        } catch (error) {
            console.error(error);
        }
    }

    async onClickmatches() {
        try {
            await this.action.doAction("bc_sport.action_bc_sport_matches");
        } catch (error) {
            console.error(error);
        }
    }

    async onClickLeaderboard() {
        try {
            await this.action.doAction("bc_sport.action_bc_sport_leaderboard");
        } catch (error) {
            console.error(error);
        }
    }

    async onClickNewMatch(type) {
        const validTypes = ["1v1", "2v2"];
        if (validTypes.includes(type)) {
            window.location.href = `/ping-pong/match?type=${type}`;
        }
    }

    async onClickCreatePlayer() {
        try {
            await this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "bc_sport.player",
                views: [[false, "form"]],
                target: "current",
            });
        } catch (error) {
            console.error(error);
        }
    }
}

registry.category("actions").add("bc_sport.dashboard", Dashboard);
