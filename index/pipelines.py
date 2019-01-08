# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import numpy
import re
import datetime

class IndexPipeline(object):

    def process_item(self, item, spider):
        appid = item['appid']

        if 'review_title' in item:
            if item['review_title'] and item['review_people']:
                review_people_array = re.findall(r'\d+', item['review_people'])
                review_people = review_people_array[0]+review_people_array[1]
                review_title = item['review_title']
                percentage = re.findall(r'\d+%', item['percentage'])[0]
                
                item['db'].table('game_lists').where('appid', appid).update({
                    'steam_user_review_score': percentage,
                    'steam_user_review_count': review_people,
                    'steam_user_review_summary': review_title
                })

                select_data = item['db'].table('game_reviews').where({
                    'appid': appid,
                    'summary': review_title,
                    'count': review_people,
                    'score': percentage
                }).first()
                if select_data:
                    if select_data['summary'] == review_title and select_data['count'] == review_people:
                        pass
                    else:
                        item['db'].table('game_reviews').insert({
                            'appid': appid,
                            'summary': review_title,
                            'count': review_people,
                            'score': percentage,
                            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                else:
                    item['db'].table('game_reviews').insert({
                        'appid': appid,
                        'summary': review_title,
                        'count': review_people,
                        'score': percentage,
                        'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            else:
                pass

        if 'tag' in item:
            if item['tag']:
                for data in item['tag']:
                    select_data = item['db'].table('game_tags').where({
                        'appid': appid,
                        'tag': data.strip()
                    }).first()
                    if select_data:
                        if select_data['tag'] == data.strip():
                            pass
                        else:
                            item['db'].table('game_tags').insert({
                                'appid': appid,
                                'tag': data.strip(),
                                'language': 'schinese',
                                'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                    else:
                        item['db'].table('game_tags').insert({
                            'appid': appid,
                            'tag': data.strip(),
                            'language': 'schinese',
                            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })

            else:
                pass
                    
        else:
            if item['jsonresponse'][appid]['success']:
                api_data = item['jsonresponse'][appid]['data']
                if 'name' in api_data:
                    select_data = item['db'].table('game_lists').where({
                        'appid': appid,
                    }).first()
                    
                    if select_data:
                        item['db'].table('game_lists').where('appid', appid).update({
                            'name': api_data['name'],
                            'updated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })

                    else:
                        item['db'].table('game_lists').insert({
                            'appid': appid,
                            'name': api_data['name'],
                            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                    
                    if 'required_age' in api_data:
                        item['db'].table('game_lists').where('appid', appid).update({
                            'age': api_data['required_age']
                        })
                    
                    if 'is_free' in api_data:
                        item['db'].table('game_lists').where('appid', appid).update({
                            'free': api_data['is_free']
                        })

                    if 'detailed_description' in api_data:
                        item['db'].table('game_lists').where('appid', appid).update({
                            'detailed_description': api_data['detailed_description']
                        })

                    if 'short_description' in api_data:
                        item['db'].table('game_lists').where('appid', appid).update({
                            'short_description': api_data['short_description']
                        })

                    if 'platforms' in api_data:
                        platform_linux = ''
                        platform_windows = ''
                        platform_mac = ''
                        if api_data['platforms']['windows']:
                            platform_windows = 'windows|'
                        if api_data['platforms']['mac']:
                            platform_mac = 'mac|'
                        if api_data['platforms']['linux']:
                            platform_linux = 'linux|'
                        platforms = platform_mac + platform_windows + platform_linux
                        item['db'].table('game_lists').where('appid', appid).update({
                            'platforms': platforms
                        })

                    if 'supported_languages' in api_data:
                        item['db'].table('game_lists').where('appid', appid).update({
                            'languages': api_data['supported_languages']
                        })

                    if 'genres' in api_data:
                        item['db'].table('game_lists').where('appid', appid).update({
                            'type': api_data['genres'][0]['description']
                        })

                    if 'metacritic' in api_data:
                        metacritic_dict = api_data['metacritic']
                        item['db'].table('game_lists').where('appid', appid).update({
                            'metacritic_review_score': metacritic_dict['score'].__str__(),
                            'metacritic_review_link': metacritic_dict['url']
                        })

                    if 'developers' in api_data:
                        item['db'].table('game_lists').where('appid', appid).update({
                            "developers": api_data['developers']
                        })

                    if 'developers' in api_data:
                        item['db'].table('game_lists').where('appid', appid).update({
                            "developers": api_data['developers'][0],
                            "publishers": api_data['publishers'][0]
                        })

                    if 'release_date' in api_data:
                        release_date_dict = api_data['release_date']
                        release_date = release_date_dict['date']
                        pattern = re.compile(r'\d+')
                        parse_date = pattern.findall(release_date)
                        item['db'].table('game_lists').where('appid', appid).update({
                            'released_at': datetime.datetime(int(parse_date[0]), int(parse_date[1]), int(parse_date[2]), 0, 0, 0, 0)
                        })

                    if 'price_overview' in api_data:
                        price_overview = api_data['price_overview']

                        select_data = item['db'].table('game_prices').where({
                            'appid': appid,
                            'final': price_overview['final'],
                        }).first()

                        if price_overview:
                            item['db'].table('game_lists').where('appid', appid).update({
                                "price_final": price_overview['final'],
                                "price_initial": price_overview['initial'],
                                'price_discount': price_overview['discount_percent'],
                                'updated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })

                        if select_data:
                            pass

                        else:
                            if price_overview:
                                item['db'].table('game_prices').insert({
                                    'appid': appid,
                                    'country': 'china',
                                    'final': price_overview['final'],
                                    'initial': price_overview['initial'],
                                    'discount': price_overview['discount_percent'],
                                    'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                })