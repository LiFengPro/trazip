import requests
import json
import time
import unittest
import logging
import re
from urllib.parse import urljoin


class CtripHotels(object):
    """ Spider for scrapying infos from hotels.ctrip.com .

    Attributes:
        logger: logger instance.
        base_url: base_url of ctrip.com
    """
    def __init__(self):
        """Inits CtripHotels."""
        self.logger = logging.Logger('spider')
        self.base_url = 'http://hotels.ctrip.com'

    def get_cities(self):
        """ Get cities info from ctrip.com, recording city_id in this site.

        Using api /Domestic/Tool/AjaxGetCitySuggestion.aspx to get info about cities.
        Example response:
            if (!cQuery.jsonpResponse) { cQuery.jsonpResponse = {}; } cQuery.jsonpResponse
            .suggestion={热门:[{display:"北京",data:"Beijing|北京|1",group:"B"},...
        """
        city_suggestion_api = 'Domestic/Tool/AjaxGetCitySuggestion.aspx'
        response = requests.get(url=urljoin(self.base_url, city_suggestion_api))

        ctrip_id_pattern_in_data = re.compile(r'\|(\d+)$')
        name_pattern_in_data = re.compile(r"^(\w+'?\s?\w*)\|")

        # Convert response to standard json format.
        content = response.text
        start = content.find('suggestion=') + len('suggestion=')
        content = content[start: ]
        replacements = ['热门', 'display', 'data', 'group', 'ABCD', 'EFGH',
                        'JKLM', 'NOPQRS', 'TUVWX', 'YZ']
        for replacement in replacements:
            content = content.replace(replacement, '"{}"'.format(replacement))
        content = json.loads(content)

        cities = []
        for value in content.values():
            for city in value:
                chinese_name = city['display']
                match = ctrip_id_pattern_in_data.search(city['data'])
                if match:
                    ctrip_id = match.group(1)
                else:
                    self.logger.critical('Fail to find ctrip_id of city {}'.format(chinese_name))
                match = name_pattern_in_data.search(city['data'])
                if match:
                    name = match.group(1)
                else:
                    self.logger.critical('Fail to find name of city {}'.format(chinese_name))

                city_dict = {
                    'name': name,
                    'ctrip_id': int(ctrip_id),
                    'chinese_name': chinese_name
                    }
                cities.append(city_dict)
        return cities

    def get_hotel_list(self, city_id='', star=0, counts=0):
        """ Get hotel info from hotels.ctrip.com.

        Args:
            city_id (int): city_id in ctrip.com.
            star (int): Star of hotels, from 0 to 5
            counts (int): Numbers of hotels to get.
        """
        response = self._request_hotel_list(city_id=city_id, star=star)
        total_amount = response['hotelAmount']
        if counts >= total_amount:
            self.logger.debug('Only {} hotels match all conditions, input {} exceeds.'
                              .format(total_amount, counts))
            counts = total_amount
        elif counts == 0:
            counts = total_amount

        hotels_name = []
        for page in range(1, (counts-1)//25+2):
            time.sleep(3)
            self.logger.debug('Downloading Page {}....'.format(page))
            response = self._request_hotel_list(city_id=city_id, star=star, page=page)
            if len(response['hotelPositionJSON']) == 0:
                break
            for hotel_detail in response['hotelPositionJSON']:
                hotels_name.append(hotel_detail['name'])
        return hotels_name[0:counts]

    def _request_hotel_list(self, city_id='', page=1, star=0):
        """ Request hotel list from hotels.ctrip.com.

        Args:
            city_id (int): city_id in ctrip.com.
            page (int): Page #.
            star (int): Star of hotels, from 0 to 5.
        """
        hotel_list_api = 'Domestic/Tool/AjaxHotelList.aspx'
        payload = {
            'star': star,
            'cityId': city_id,
            'page': page, #page, # 25 items per page
        }

        response = requests.post(
            url=urljoin(self.base_url, hotel_list_api),
            data=payload
        )

        response = json.loads(response.text)
        return response
