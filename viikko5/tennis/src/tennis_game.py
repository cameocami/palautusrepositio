class TennisGame:
    SCORE_NAMES = ["Love", "Fifteen", "Thirty", "Forty"]
    def __init__(self, player1_name: str, player2_name: str) -> None:
        self.player1 = {"name": player1_name, "points": 0}
        self.player2 = {"name": player2_name, "points": 0}
    

    def won_point(self, player_name) -> None:
        if player_name == self.player1["name"]:
            self.player1["points"] += 1
        else:
            self.player2["points"] += 1

    @property
    def difference(self) -> int:
        return self.player1["points"] - self.player2["points"]

    @property
    def is_endgame(self) -> bool:
        return self.player1["points"] >= 4 or self.player2["points"] >= 4

    def _endgame_score(self) -> str:
        if self.difference == 1:
            return f"Advantage {self.player1['name']}"
        if self.difference == -1:
            return f"Advantage {self.player2['name']}"
        if self.difference >= 2:
            return f"Win for {self.player1['name']}"
        return f"Win for {self.player2['name']}"


    def get_score(self) -> str:

        if self.player1["points"] == self.player2["points"]:
            if self.player1["points"] < 3:
                return self.SCORE_NAMES[self.player1["points"]] + "-All"
            return "Deuce"
        elif self.is_endgame:
            return self._endgame_score()
        else:
            return self.SCORE_NAMES[self.player1["points"]] + "-" + self.SCORE_NAMES[self.player2["points"]]

