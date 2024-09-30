from odoo import models, fields, api, _

RANKS = [
    ("10_tourist", "10. Tourist"),
    ("9_ball_collector", "9. Ball Collector"),
    ("8_sunday_player", "8. Sunday Player"),
    ("7_smash_princess", "7. Smash Princess"),
    ("6_garage_warrior", "6. Garage Warrior"),
    ("5_racket_ninja", "5. Racket Ninja"),
    ("4_smash_virtuoso", "4. Smash Virtuoso"),
    ("3_ball_tamer", "3. Ball Tamer"),
    ("2_king_of_ping", "2. King of Ping"),
    ("1_ping_master", "1. Ping Master"),
]


class Player(models.Model):
    _name = "bc_sport.player"

    # Unique username and unique partner
    _sql_constraints = [
        ("name_uniq", "unique(name)", _("Username must be unique")),
        (
            "partner_id_uniq",
            "unique(partner_id)",
            _("Partner can only have one player"),
        ),
    ]

    @api.depends("match_ids")
    def _compute_match_count(self):
        for rec in self:
            rec.match_count = len(rec.match_ids)
            rec.match_won_count = len(
                rec.match_ids.filtered(lambda match: match.winner_ids in rec)
            )
            rec.match_lost_count = len(
                rec.match_ids.filtered(lambda match: match.looser_ids in rec)
            )
            rec.ratio = (
                rec.match_won_count / rec.match_count * 100
                if rec.match_count
                else 0
            )

    @api.depends("match_ids")
    def _compute_matches(self):
        for rec in self:
            rec.match_ids = self.env["bc_sport.match"].search(
                ["|", ("player_1", "=", rec.id), ("player_2", "=", rec.id)]
            )

    @api.depends("match_ids")
    def _compute_streak(self):
        for rec in self:
            rec.streak = 0

            # Guard clause to ensure matches are present
            if not rec.match_ids:
                continue

            # Sort matches by date inverse
            matches = rec.match_ids.sorted(key=lambda r: r.date, reverse=True)

            # Determine the current streak type (winner or looser)
            current_result = (
                "winner" if matches[0].winner_ids in rec else "looser"
            )

            # Function to check if match is a win or a loss
            def is_winner(match):
                return match.winner_ids in rec

            def is_looser(match):
                return match.looser_ids in rec

            # Calculate the streak
            for match in matches:
                if current_result == "winner" and is_winner(match):
                    rec.streak += 1
                elif current_result == "looser" and is_looser(match):
                    rec.streak -= 1
                else:
                    break  # End the streak if the pattern breaks

    @api.depends("match_won_count", "match_lost_count")
    def _compute_rank(self):
        for rec in self:
            rec.rank = RANKS[0][0]

    name = fields.Char(string="Username", required=True)
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
        domain="[('is_company', '=', False)]",
    )
    avatar = fields.Image(string="Avatar")

    match_ids = fields.Many2many(
        comodel_name="bc_sport.match",
        compute="_compute_matches",
        string="Matches",
    )
    match_count = fields.Integer(
        string="Match Count", compute="_compute_match_count"
    )
    match_won_count = fields.Integer(
        string="Match Won Count", compute="_compute_match_count"
    )
    match_lost_count = fields.Integer(
        string="Match Lost Count", compute="_compute_match_count"
    )
    ratio = fields.Integer(string="Ratio", compute="_compute_match_count")
    streak = fields.Integer(string="Streak", compute="_compute_streak")
    rank = fields.Selection(
        selection=RANKS,
        string="Rank",
        default="10_tourist",
        readonly=True,
        compute="_compute_rank",
    )
