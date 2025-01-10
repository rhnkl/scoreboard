from PIL import Image, ImageDraw

from board_manager import Scoreboard

def resize_team_logo(image_path, size) -> Image:
    with Image.open(image_path) as im:
        im.thumbnail(size, Image.Resampling.LANCZOS)
        return im

class ScoreboardImage:
    def __init__(self, image_path, reference_board: Scoreboard, home_color: tuple = (0, 51, 0), away_color: tuple = (0, 0, 51)):
        self.image_path = image_path
        self.board = reference_board

        self.home_color = home_color
        self.away_color = away_color

        if (0.2126 * home_color[0])+(0.7152 * home_color[1])+(0.0722 * home_color[2]) < 128:
            self.home_text_color = (255, 255, 255)
        else:
            self.home_text_color = (0, 0, 0)

        if (0.2126 * away_color[0])+(0.7152 * away_color[1])+(0.0722 * away_color[2]) < 128:
            self.away_text_color = (255, 255, 255)
        else:
            self.away_text_color = (0, 0, 0)

    def update_scoreboard(self, board: Scoreboard) -> Image:
        home_score = board.get_score('home')
        away_score = board.get_score('away')
        home_fouls = board.get_fouls('home')
        away_fouls = board.get_fouls('away')
        home_largest_player_foul = board.get_largest_player_foul('home')
        away_largest_player_foul = board.get_largest_player_foul('away')
        state = board.get_state()

        with Image.open(self.image_path) as im:
            im = im.convert('RGBA')
            im = im.resize((1920, 1080))
            im = im.convert('RGB')
            im.paste((0, 255, 0), (0, 0, 1920, 1080))

            # Create a lower-third scoreboard with all the stats provided.
            ImageDraw.Draw(im).rectangle((1541, 851, 1803, 1005), fill=(230, 230, 230), outline=(0, 0, 0), width=1)
            ImageDraw.Draw(im).line((1618, 851, 1618, 1005), fill=(0, 0, 0), width=1)
            ImageDraw.Draw(im).line((1727, 851, 1727, 1005), fill=(0, 0, 0), width=1)
            ImageDraw.Draw(im).line((1541, 927, 1803, 927), fill=(0, 0, 0), width=1)
            ImageDraw.Draw(im).rectangle((1803, 895, 1869, 961), fill=(230, 230, 230), outline=(0, 0, 0), width=1)

            ImageDraw.Draw(im).rectangle((1542, 928, 1617, 1004), fill=self.home_color)
            ImageDraw.Draw(im).rectangle((1728, 928, 1802, 1004), fill=self.home_color)

            ImageDraw.Draw(im).text((1671, 889), f'{away_score}', fill=(0, 0, 0), anchor="mm", font_size=60)
            ImageDraw.Draw(im).text((1671, 966), f'{home_score}', fill=(0, 0, 0), anchor="mm", font_size=60)

            ImageDraw.Draw(im).text((1836, 928), f'{state}', fill=(0, 0, 0), anchor="mm", font_size=30)

            ImageDraw.Draw(im).text((1765, 889), f'TF {away_fouls}', fill=(0, 0, 0), anchor="mm", font_size=30)
            ImageDraw.Draw(im).text((1765, 966), f'TF {home_fouls}', fill=self.home_text_color, anchor="mm", font_size=30)

            # Overlay team logos on scoreboard. respect transparency of the logos.
            home_logo = resize_team_logo('home_logo.png', (75, 76))
            home_w, home_h = home_logo.size
            home_y_pos = 928 + ((76 - home_h) // 2)
            home_x_pos = 1542 + ((75 - home_w) // 2)

            away_logo = resize_team_logo('away_logo.png', (75, 75))
            away_w, away_h = away_logo.size
            away_y_pos = 852 + ((76 - away_h) // 2)
            away_x_pos = 1542 + ((75 - away_w) // 2)

            im.paste(home_logo, (home_x_pos, home_y_pos), home_logo)
            im.paste(away_logo, (away_x_pos, away_y_pos), away_logo)

            if home_largest_player_foul["player"] is not None:
                ImageDraw.Draw(im).rectangle((1579, 813, 1765, 851), fill=self.home_color)
                ImageDraw.Draw(im).text((1672, 832), f'#{home_largest_player_foul["player"]}: Foul {home_largest_player_foul["foul_count"]}', fill=self.home_text_color, anchor="mm", font_size=30)

            if away_largest_player_foul["player"] is not None:
                ImageDraw.Draw(im).rectangle((1579, 1005, 1765, 1042), fill=self.away_color)
                ImageDraw.Draw(im).text((1672, 1024), f'#{away_largest_player_foul["player"]}: Foul {away_largest_player_foul["foul_count"]}', fill=self.away_text_color, anchor="mm", font_size=30)

            im.save(self.image_path)
            return im