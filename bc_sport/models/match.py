from odoo import models, fields, api


class Match(models.Model):
    _name = "bc_sport.match"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc"

    @api.depends("player_1", "player_2")
    def _compute_display_name(self):
        for record in self:
            record.display_name = (
                f"{record.player_1.name} vs {record.player_2.name}"
            )
            record.name = record.display_name

    @api.depends("score_1", "score_2")
    def _compute_winner(self):
        for record in self:
            if record.match_type == "simple":
                if record.score_1 > record.score_2:
                    record.winner_ids = record.player_1
                    record.looser_ids = record.player_2
                else:
                    record.winner_ids = record.player_2
                    record.looser_ids = record.player_1
            else:
                if record.score_1 > record.score_2:
                    record.winner_ids = record.team_1
                    record.looser_ids = record.team_2
                else:
                    record.winner_ids = record.team_2
                    record.looser_ids = record.team_1

    display_name = fields.Char(
        string="Match", compute="_compute_display_name", store=True
    )
    name = fields.Char(
        string="Match Name", compute="_compute_display_name", store=True
    )

    player_1 = fields.Many2one(
        comodel_name="bc_sport.player",
        string="Player 1",
        domain="[('id', '!=', player_2)]",
        tracking=True,
    )
    player_1_avatar = fields.Image(
        related="player_1.avatar", string="Avatar Player 1"
    )
    player_2 = fields.Many2one(
        comodel_name="bc_sport.player",
        string="Player 2",
        domain="[('id', '!=', player_1)]",
        tracking=True,
    )
    player_2_avatar = fields.Image(
        related="player_2.avatar", string="Avatar Player 2"
    )

    score_1 = fields.Integer(string="Score Player/Team 1", tracking=True)
    score_2 = fields.Integer(string="Score Player/Team 2", tracking=True)

    winner_ids = fields.Many2many(
        comodel_name="bc_sport.player",
        string="Winner",
        compute="_compute_winner",
    )
    looser_ids = fields.Many2many(
        comodel_name="bc_sport.player",
        string="Looser",
        compute="_compute_winner",
    )

    date = fields.Datetime(
        string="Date",
        default=lambda self: fields.datetime.now(),
        readonly=True,
    )

    match_type = fields.Selection(
        selection=[("simple", "Simple"), ("double", "Double")],
        string="Match Type",
        default="simple",
        readonly=True,
    )

    team_1 = fields.Many2many(
        comodel_name="bc_sport.player",
        relation="match_team_1_rel",
        column1="match_id",
        column2="player_id",
        string="Team 1",
        tracking=True,
    )
    team_2 = fields.Many2many(
        comodel_name="bc_sport.player",
        relation="match_team_2_rel",
        column1="match_id",
        column2="player_id",
        string="Team 2",
        tracking=True,
    )
