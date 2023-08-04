from datetime import timedelta
from datetime import datetime as dt
import re
import requests
from rich import print as rprint


class LoLFandomHandler:

    def __init__(self) -> None:
        pass

    def get_matches(self) -> dict:
        params = {
            'SFS[1]': 'LCS/2023 Season/Summer Season',
            '_run': '',
            'pfRunQueryFormName': 'SpoilerFreeSchedule',
            'wpRunQuery': '',
            'pf_free_text': '',
        }
        response = requests.get(
            'https://lol.fandom.com/wiki/Special:RunQuery/SpoilerFreeSchedule',
            params=params,
        )
        if response and response.status_code == 200:
            data = response.text
            match_block_reg = '(Week \d+.*?class="team-object".*?<\/tr>)'
            matches = re.findall(match_block_reg, data)
            for match in matches:
                week_reg = '(Week\s\d+)'
                team_reg = 'class="team-object">.*?href.*?title="(.*?)"'
                datetime_reg = 'class="TimeInLocal">(.*?)<\/span>'
                stream_link_reg = 'rel="nofollow noreferrer noopener".*?href="(.*?)"'
                week = re.search(week_reg, match).group(1)
                teams = re.findall(team_reg, match)
                datetime = re.search(datetime_reg, match).group(1)
                date_obj = dt.strptime(datetime, "%Y,%m,%d,%H,%M")
                local_date_obj = date_obj + timedelta(hours=3)
                stream_link = re.search(stream_link_reg, match).group(1)
                rprint(
                    f'{week} {teams[0]} vs {teams[1]} {local_date_obj} {stream_link}')
                # Открытие файла для записи
                with open("matches.txt", "a") as file:
                    # Запись данных в файл
                    file.write(
                        f'{week} {teams[0]} vs {teams[1]} {local_date_obj} {stream_link}\n')


if __name__ == '__main__':
    fandom = LoLFandomHandler()
    fandom.get_matches()
