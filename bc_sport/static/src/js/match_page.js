/** @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";

publicWidget.registry.BcSportMatch = publicWidget.Widget.extend({
    selector: ".bc_sport_match",
    events: {
        "change #player-1,#player-2": "onChangePlayer",
        "focus input.score-player-1,input.score-player-2": "onFocusInput",
        "keypress input.score-player-1,input.score-player-2": "onChangeScore",
        // Press button
        "click .btn-score": "onChangeScore",
    },

    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
    },

    /**
     * @override
     */
    start() {
        document.getElementById("footer").style.display = "none";

        this.player1Select = this.$("#player-1");
        this.player2Select = this.$("#player-2");
    },

    /**
     *
     * @param {Event} ev
     */
    async onChangePlayer(ev) {
        console.log("onChangePlayer", ev);

        const player1 = this.player1Select.find(":selected");
        const player1avatar = this._getAvatarUrl(player1.data("avatar"));
        const player2 = this.$("#player-2");
        const player2avatar = this._getAvatarUrl(player2.data("avatar"));

        const $avatar1 = this.$("#avatar-player-1");
        const $avatar2 = this.$("#avatar-player-2");

        var style1 = $avatar1.attr("style");
        var style2 = $avatar2.attr("style");

        // Get the background image url from the style attribute
        var url1 = style1.match(/url\(["']?([^"']*)["']?\)/);
        var url2 = style2.match(/url\(["']?([^"']*)["']?\)/);

        // If the url is not null, then we need to replace the url with the new avatar
        if (url1) {
            $avatar1.css("background-image", `url(${player1avatar})`);
        }
        if (url2) {
            $avatar2.css("background-image", `url(${player2avatar})`);
        }

        const player1name = this.$("#name-player-1");
        const player2name = this.$("#name-player-2");

        player1name.text(
            player1.text() === "Select a player"
                ? _t("PLAYER 1")
                : player1.text()
        );
        player2name.text(
            player2.text() === "Select a player"
                ? _t("PLAYER 2")
                : player2.text()
        );
    },

    /**
     *
     * @param {Event} ev
     */
    async onFocusInput(ev) {
        ev.target.select();
    },

    /**
     * @param {Event} ev
     */
    async onChangeScore(ev) {
        // console.log("onChangeScore", ev);

        if (ev.type === "click") {
            ev.preventDefault();
        } else if (ev.type === "keypress") {
            console.log("key", ev.key);
        }

        console.log(this.$("input.score-player-1.score-center").val());

        if (
            this.player1Select.find(":selected").val() === "False" ||
            this.player2Select.find(":selected").val() === "False"
        ) {
            // TODO: Modal to display the error
            alert("Please select two players before changing the score");
            return;
        }

        this.changeScore(ev);

        if (
            this.$("input.score-player-1.score-center").val() != "0" ||
            this.$("input.score-player-2.score-center").val() != "0"
        ) {
            // Disable the select
            console.log("Disable the select");

            this.player1Select.attr("disabled", true);
            this.player2Select.attr("disabled", true);
        } else {
            console.log("Enable the select");

            this.player1Select.attr("disabled", false);
            this.player2Select.attr("disabled", false);
        }
    },

    /**
     *
     * @param {Event} ev
     */
    async changeScore(ev) {
        console.log("changeScore", ev);

        const $input = ev.target.classList.contains("player-1")
            ? this.$("input.score-player-1.score-center")
            : this.$("input.score-player-2.score-center");

        console.log("input", $input);

        if (ev.type === "click") {
            if (ev.target.classList.contains("minus")) {
                // If the input value is 0, then we don't want to go below 0
                $input.val(Math.max(0, parseInt($input.val()) - 1));
            } else {
                $input.val(parseInt($input.val()) + 1);
            }
        }
    },

    _getAvatarUrl(avatar) {
        if (avatar) {
            // Need to add the prefix to the base64 string and remove the b' from the string and the ' at the end
            return (
                "data:image/png;base64," +
                avatar.replace("b'", "").replace("'", "")
            );
        }
        return "/bc_sport/static/src/img/default_avatar.png";
    },
});
