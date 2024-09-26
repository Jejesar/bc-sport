from odoo import http
from odoo.http import request, route, Controller


class PingPong(Controller):
    @route("/ping-pong/test", auth="public", type="http")
    def test(self, **kwargs):
        return "PingPong Test"

    @route("/ping-pong/match", auth="user", type="http", website=True)
    def new(self, **kwargs):

        player_ids = request.env["bc_sport.player"].search([])

        return request.render(
            "bc_sport.pingpong_match_page",
            {
                "match_type": request.params.get("match_type", "1v1"),
                "players": player_ids,
            },
        )
