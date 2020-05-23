from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
from model import Game
from mongo import Mongo
from datetime import datetime

class SteamParser(object):

  def parse(self):
    requests_arr = ['https://store.steampowered.com/search/results/?query&start=' +str(page_number*50) +
                '&count=50&cc=US&l=english&sort_by=_ASC' for page_number in range(50)]
    with Pool(30) as p:
      p.map(self.make_all, requests_arr)


  def make_all(self, requests):
    html = self.get_html(requests)
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', id="search_resultsRows")
    links = [a['href'][:a['href'].rfind('/')] for a in div.find_all('a')]
    title = [a.text.strip() for a in div.find_all('span', class_='title')]
    release_dates = [a.text for a in div.find_all('div', class_='search_released')]
    prices = [a.text.strip()
              if a.text.find('$') == -1 or a.text.find('$', a.text.find('$') + 1) == -1
              else a.text[a.text.rfind('$'):].strip()
              for a in div.find_all('div', class_='search_price')]

    for i, link in enumerate(links):
      try:
        game = Game()
        game.title = title[i]
        game.release_date = datetime.strptime(release_dates[i].replace(',', ''), '%b %d %Y').strftime('%d.%m.%Y')
        game.price = 0.0 if prices[i] == 'Free to Play' else float(prices[i][1:])
        self.get_page_game(link, game)
        Mongo.write_mongo(game)
      except Exception as ex:
        print(ex, link)


  def get_html(self, url):
    with requests.Session() as session:
        cookies= {'birthtime': '975621601', 'lastagecheckage': '1-0-2001'}
        response = session.get(url, cookies = cookies)
    return response.text


  def get_page_game(self, link, game):
    html = self.get_html(link)
    soup = BeautifulSoup(html, 'lxml')
    game.url_photo = soup.find('img', class_="game_header_image_full")['src']
    game.genre = soup.find('div', class_='block_content_inner').find('a').text
    game.description = soup.find('div', class_='game_description_snippet') \
      .text.replace('\r', '').replace('\t', '').replace('\n', '')
    game.developer = soup.find('div', id='developers_list').text.strip()
    game.publisher = soup.find('div', class_='dev_row').find('a').text.strip()
    try:
      system_requirment = soup.find('div', class_='game_area_sys_req_leftCol').find('ul', class_='bb_ul').text
    except:
      system_requirment = soup.find('div', class_='game_area_sys_req_full').find('ul', class_='bb_ul').text
    game.operating_system = system_requirment[system_requirment.find('OS:') + 3:
                                              system_requirment.find('Processor:')].strip().split(',')
    try:
      game.processor = system_requirment[system_requirment.find('Processor:') + 10:
                                         system_requirment.find('Memory:')].split(' or ').remove('better')
    except:
      game.processor = system_requirment[system_requirment.find('Processor:') + 10:
                                         system_requirment.find('Memory:')].split(' or ')
    game.memory = system_requirment[system_requirment.find('Memory:') + 7: system_requirment.find('RAM') + 3].strip()
    try:
      game.graphics = system_requirment[system_requirment.find('Graphics:') + 9:
                                        system_requirment.find('DirectX:')].strip().split(' or ').remove('better')
    except:
      game.graphics = system_requirment[system_requirment.find('Graphics:') + 9:
                                        system_requirment.find('DirectX:')].split(' or ')
    if system_requirment.find('Storage:') != -1:
      game.storage = system_requirment[system_requirment.find('Storage:') + 8: system_requirment.rfind('GB') + 2]
    game.language = [a.find('td').text.replace('\r', '').replace('\t', '').replace('\n', '')
                     for a in soup.find('table', class_='game_language_options').find_all('tr')[1:]]

    rating_line = soup.find('span', class_='nonresponsive_hidden responsive_reviewdesc').text
    game.rating = int(rating_line[rating_line.find(' '): rating_line.find('%')])
    game.url_steam = link
