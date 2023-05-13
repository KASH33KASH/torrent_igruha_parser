import requests
from bs4 import BeautifulSoup
from FakeAgent import Fake_Agent
import time


fake_agent = Fake_Agent().random()

header = {
    "user-agent": fake_agent
}

def main():
    page = 1
    game_count = 0
    for pages in range(227):
        url = f"https://it.itorrents-igruha.org/newgames/page/{page}/"

        html_code = requests.get(url, headers=header).text
        soup = BeautifulSoup(html_code, "lxml")

        game_block = soup.find("div", class_="articles-film-cuted")
        games = game_block.find_all("div", class_="article-film")

        for game in games:
            game_name = game.find("div", class_="article-film-title")
            game_url = game_name.find("a").get("href")

            html_game = requests.get(game_url, headers=header).text
            game_soup = BeautifulSoup(html_game, "lxml")

            game_info_block = game_soup.find("div", id="dle-content")
            game_info = game_info_block.find("div", style="padding-left: 215px;")

            game_info = str(game_info).replace('<div class="exampleone">', '')
            game_info = game_info.replace('<div style="padding-left: 215px;">', '')
            game_info = game_info.replace('</div>', '').strip()
            game_info = game_info.replace('<b>', '')
            game_info = game_info.replace('</b>', '')

            if '<hr class="light2"/><center>' in game_info:
                if '\n    \n  \n    \n\n<hr class="light2"/><center>' in game_info:
                    game_info = game_info[:game_info.index('\n    \n  \n    \n\n<hr class="light2"/><center>'):]
                else:
                    game_info = game_info[:game_info.index('<hr class="light2"/><center>'):]

            game_info = game_info.split("<br/>")

            with open("GameList.txt", "a", encoding='utf-8') as f:
                f.write(game_name.text + "\n")
                f.write("\n")

            for el in game_info:
                with open("GameList.txt", "a", encoding='utf-8') as file:
                    file.write(el + "\n")
            with open("GameList.txt", "a", encoding='utf-8') as file:
                file.write(2 * "\n")
            game_count += 1
            print(f"Found games: {game_count}")
        page += 1
    print(f"Found {game_count} games")


start_time = time.time()

main()

close_time = time.time()
work_time = close_time - start_time
if work_time > 60:
    print(f"Work time {round(work_time / 60, 2)} minutes")
elif work_time > 3600:
    print(f"Work time {round(work_time / 60 / 60, 2)} hours")
else:
    print(f"Work time {round(work_time, 2)} seconds")
