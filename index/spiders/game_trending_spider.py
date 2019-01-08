# coding: UTF-8
import scrapy
import json
import re
import datetime
from scrapy.http.request import Request
from orator import DatabaseManager


class GameTrending(scrapy.Spider):
    name = "game_trending"
    start_urls = [
        'https://store.steampowered.com/stats/',
    ]

    def parse(self, response):
        db_config = self.settings.get('DB')
        config = {
            'mysql': {
                'driver': db_config['driver'],
                'host': db_config['host'],
                'port': db_config['port'],
                'database': db_config['database'],
                'user': db_config['user'],
                'password': db_config['password'],
                'prefix': db_config['prefix']
            }
        }

        db = DatabaseManager(config)
        datetime_utc_plus8 = datetime.datetime.utcnow() + datetime.timedelta(hours=+8)
        datetime_parse = datetime_utc_plus8.strftime('%Y-%m-%d %H:%M:00')
        for element in response.css('.player_count_row'):
          now_split = element.css('td:nth-child(1) > span::text').extract_first()
          now_array = now_split.split(',')
          now = now_array[0] + now_array[1]
          total_split = element.css('td:nth-child(2) > span::text').extract_first()
          total_array = total_split.split(',')
          total = total_array[0] + total_array[1]
          title = element.css('td:nth-child(4) > a::text').extract_first()
          link = element.css('td:nth-child(4) > a::attr(href)').extract_first()
          appid = re.search('-?[1-9]\d*',link).group(0)
          select_data = db.table('game_hots').where({
              'appid': appid,
              'name': title
          }).order_by('created_at', 'desc').first()

          if select_data:
            if now == select_data['current'] and total == select_data['total']:
              pass
            else:
              db.table('game_hots').insert({
                  'appid': appid,
                  'name': title,
                  'total': str(total),
                  'current': str(now),
                  'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:00')
              })
          else:
            db.table('game_hots').insert({
                'appid': appid,
                'name': title,
                'total': total,
                'current': now,
                'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:00')
            })