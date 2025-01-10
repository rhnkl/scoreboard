class Scoreboard:
    def __init__(self):

        self.home_team_score: int = 0
        self.away_team_score: int = 0

        self.home_team_fouls: int = 0
        self.away_team_fouls: int = 0

        self.home_team_player_fouls = []
        self.away_team_player_fouls = []

        self.scoreboard_state = 'Q1'

    def score(self, team: str, points: int) -> int:
        if team == 'home':
            self.home_team_score += points
            return self.home_team_score
        elif team == 'away':
            self.away_team_score += points
            return self.away_team_score

    def foul(self, team: str, amount: int = 1):
        if team == 'home':
            self.home_team_fouls += amount
        elif team == 'away':
            self.away_team_fouls += amount

    def player_foul(self, team: str, player: int, amount: int = 1):
        if team == 'home':
            for fouled_player in self.home_team_player_fouls:
                if fouled_player['player'] == player:
                    fouled_player['foul_count'] += amount
                    return
            self.home_team_player_fouls.append({'player': player, 'foul_count': amount})
        elif team == 'away':
            for fouled_player in self.away_team_player_fouls:
                if fouled_player['player'] == player:
                    fouled_player['foul_count'] += amount
                    return
            self.away_team_player_fouls.append({'player': player, 'foul_count': amount})

    def set_state(self, state: str):
        self.scoreboard_state = state

    def get_state(self) -> str:
        return self.scoreboard_state

    def get_score(self, team: str):
        if team == 'home':
            return self.home_team_score
        elif team == 'away':
            return self.away_team_score

    def get_fouls(self, team: str):
        if team == 'home':
            return self.home_team_fouls
        elif team == 'away':
            return self.away_team_fouls

    def get_player_fouls(self, team: str, player: int):
        if team == 'home':
            for fouled_players in self.home_team_player_fouls:
                if fouled_players['player'] == player:
                    return fouled_players['fouls']
        elif team == 'away':
            for fouled_players in self.away_team_player_fouls:
                if fouled_players['player'] == player:
                    return fouled_players['fouls']
        return 0

    def get_largest_player_foul(self, team: str):
        if team == 'home':
            largest_foul = {'player': None, 'foul_count': 0}
            if len(self.home_team_player_fouls) == 0:
                return largest_foul
            for fouled_players in self.home_team_player_fouls:
                if fouled_players['foul_count'] > largest_foul['foul_count']:
                    largest_foul['player'] = fouled_players['player']
                    largest_foul['foul_count'] = fouled_players['foul_count']
            return largest_foul
        elif team == 'away':
            largest_foul = {'player': None, 'foul_count': 0}
            if len(self.away_team_player_fouls) == 0:
                return largest_foul
            for fouled_players in self.away_team_player_fouls:
                if fouled_players['foul_count'] > largest_foul['foul_count']:
                    largest_foul['player'] = fouled_players['player']
                    largest_foul['foul_count'] = fouled_players['foul_count']
            return largest_foul

    def get_all_player_fouls(self, team: str):
        if team == 'home':
            return self.home_team_player_fouls
        if team == 'away':
            return self.away_team_player_fouls
        return []

    def reset(self):
        self.home_team_score = 0
        self.away_team_score = 0
        self.home_team_fouls = 0
        self.away_team_fouls = 0
        self.home_team_player_fouls = []
        self.away_team_player_fouls = []
        self.scoreboard_state = 'Q1'