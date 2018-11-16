# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import numpy
import re

class IndexPipeline(object):

    def process_item(self, item, spider):
        appid = item['appid']

        if 'review_title' in item:
            if item['review_title'] and item['review_people']:
                review_people_array = re.findall(r'\d+', item['review_people'])
                review_people = review_people_array[0]+review_people_array[1]
                review_title = item['review_title']
                percentage = re.findall(r'\d+%', item['percentage'])[0]
                select_data = item['db'].table('AppsReviews').where({
                    'AppID': appid,
                    'ReviewTitle': review_title,
                    'ReviewPeople': review_people,
                    'Percentage': percentage
                }).first()
                if select_data:
                    if select_data['ReviewTitle'] == review_title and select_data['ReviewPeople'] == review_people:
                        pass
                    else:
                        item['db'].table('AppsReviews').insert({
                            'AppID': appid,
                            'ReviewTitle': review_title,
                            'ReviewPeople': review_people,
                            'Percentage': percentage
                        })
                else:
                    item['db'].table('AppsReviews').insert({
                        'AppID': appid,
                        'ReviewTitle': review_title,
                        'ReviewPeople': review_people,
                        'Percentage': percentage
                    })
            else:
                pass

        if 'tag' in item:
            if item['tag']:
                for data in item['tag']:
                    select_data = item['db'].table('AppsTags').where({
                        'AppID': appid,
                        'Tag': data.strip()
                    }).first()
                    if select_data:
                        if select_data['Tag'] == data.strip():
                            pass
                        else:
                            item['db'].table('AppsTags').insert({
                                'AppID': appid,
                                'Tag': data.strip(),
                            })
                    else:
                        item['db'].table('AppsTags').insert({
                            'AppID': appid,
                            'Tag': data.strip(),
                        })

            else:
                pass
                    
        else:
            if item['jsonresponse'][appid]['success']:
                api_data = item['jsonresponse'][appid]['data']
                if 'name' in api_data:
                    item['db'].table('Apps').where('AppID', appid).update({
                        'StoreName': api_data['name']
                    })
                    
                    if 'required_age' in api_data:
                        item['db'].table('Apps').where('AppID', appid).update({
                            'RequiredAge': api_data['required_age']
                        })
                    
                    if 'is_free' in api_data:
                        item['db'].table('Apps').where('AppID', appid).update({
                            'Free': api_data['is_free']
                        })

                    if 'detailed_description' in api_data:
                        item['db'].table('Apps').where('AppID', appid).update({
                            'DetailedDescription': api_data['detailed_description']
                        })

                    if 'short_description' in api_data:
                        item['db'].table('Apps').where('AppID', appid).update({
                            'ShortDescription': api_data['short_description']
                        })

                    if 'platforms' in api_data:
                        chunk_platforms = numpy.vstack(api_data['platforms'])
                        platforms_array = numpy.concatenate(chunk_platforms)
                        platforms_str = '|'
                        platforms = platforms_str.join(platforms_array)
                        item['db'].table('Apps').where('AppID', appid).update({
                            'Platforms': platforms
                        })

                    if 'metacritic' in api_data:
                        metacritic_dict = api_data['metacritic']
                        metacritic = metacritic_dict['score'].__str__() + '|' + metacritic_dict['url']
                        item['db'].table('Apps').where('AppID', appid).update({
                            'Metacritic': metacritic
                        })

                    if 'release_date' in api_data:
                        release_date_dict = api_data['release_date']
                        release_date = release_date_dict['coming_soon'].__str__() + '|' + release_date_dict['date']
                        item['db'].table('Apps').where('AppID', appid).update({
                            'ReleaseDate': release_date
                        })

                    if 'price_overview' in api_data:
                        price_overview = api_data['price_overview']
                        if price_overview:
                            item['db'].table('AppsPrices').insert({
                                'AppID': appid,
                                'Country': 'China',
                                'PriceFinal': price_overview['final'],
                                'PriceInitial': price_overview['initial'],
                                'PriceDiscount': price_overview['discount_percent'],
                                'DisplayCountryName': '中国',
                                'DisplayCountrySymbol': '元'
                            })