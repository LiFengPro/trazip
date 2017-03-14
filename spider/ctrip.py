import json
import time
import unittest
import logging
import re
import string
import random
import datetime
from urllib.parse import urljoin

import requests
import execjs
from lxml import etree


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

        Using api /Domestic/Tool/AjaxGetCitySuggestion.aspx to get info about
        cities.
        Example response:
            if (!cQuery.jsonpResponse) { cQuery.jsonpResponse = {}; } cQuery.
            jsonpResponse.suggestion={热门:[{display:"北京",
            data:"Beijing|北京|1",group:"B"},...
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
                    self.logger.critical('Fail to find ctrip_id of city {}'
                                         .format(chinese_name))
                match = name_pattern_in_data.search(city['data'])
                if match:
                    name = match.group(1)
                else:
                    self.logger.critical('Fail to find name of city {}'
                                         .format(chinese_name))

                city_dict = {
                    'name': name,
                    'ctrip_id': int(ctrip_id),
                    'chinese_name': chinese_name
                    }
                cities.append(city_dict)
        return cities

    def get_hotels(self, city_id='', star=0, counts=0):
        """ Get hotels info from hotels.ctrip.com.

        Args:
            city_id (int): city_id in ctrip.com.
            star (int): Star of hotels, from 0 to 5
            counts (int): Numbers of hotels to get.
        """
        response = self._request_hotel_list(city_id=city_id, star=star)
        total_amount = response['hotelAmount']
        if counts >= total_amount:
            self.logger.debug('Only {} hotels match all conditions, '
                              'input {} exceeds.'.format(total_amount, counts))
            counts = total_amount
        elif counts == 0:
            counts = total_amount

        hotels_name = []
        for page in range(1, (counts-1)//25+2):
            self.logger.debug('Downloading Page {}....'.format(page))
            response = self._request_hotel_list(
                city_id=city_id, star=star, page=page)
            if len(response['hotelPositionJSON']) == 0:
                break
            for hotel_detail in response['hotelPositionJSON']:
                hotels_name.append(hotel_detail)
        return hotels_name[0:counts]

    def _request_hotel_list(self, city_id='', page=1, star=0):
        """ Request hotel list from hotels.ctrip.com.

        Args:
            city_id (int): city_id in ctrip.com.
            page (int): Page #.
            star (int): Star of hotels, from 0 to 5.
        Returns:
            response
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

        def repair(brokenjson):
            invalid_escape = re.compile(r"\\([^a-z\s'\"])")
            return invalid_escape.sub(r'; \1', brokenjson)

        response = json.loads(repair(response.text))
        return response

    def __gen_callback_t(self, t):
        """ Generate callback token.

        Args:
            t (int): length of token.
        Returns:
            callback token (str), starts with 'CAS'
        """
        callback = ''.join(
            [random.choice(string.ascii_letters) for i in range(t)])
        return 'CAS' + callback

    def __get_oceanball(self):
        """ Request oceanball.

        Oceanball is the tech of ctrip.com to protect their data from web spider

        Returns:
            encrypted javascript code.
        """
        oceanball_api = 'domestic/cas/oceanball'
        timestamp = int(time.time() * 1000)
        callback = self.__gen_callback_t(16)

        payload = {
            'callback': callback,
            '_': timestamp,
        }
        response = requests.get(
            url=urljoin(self.base_url, oceanball_api), params=payload)

        content = response.text
        return content

    def __decrypt_oceanball(self, content, hotel_id):
        """ Decrypt oceanball and get the value 'eleven'

        Args:
            content (str): response content after calling oceanball.
            hotel_id (int): Id of hotel.

        Returns:
            eleven_val (str): value of eleven.
        """
        match = re.search(r'fromCharCode\(item-(\d+)\)', content)
        if match:
            pwd = int(match.group(1))
        else:
            self.logger.critical('Fail to find pwd in oceanball')

        match = re.search(r'return res\}\((\[.*\])', content)
        if match:
            src = json.loads(match.group(1))
        else:
            self.logger.critical('Fail to find src in oceanball')

        src = ''.join(map(chr, [val - pwd for val in src]))

        src = src.replace('document', 'document1') # Avoid dict order affects

        replacements = {
            r'window\.Script': 'false',
            r';\!function\(\)\{': (r'function eleven(){var document1={}; '
              'var thishref="'
              + self.base_url
              + '/hotel/{}.html"; '.format(hotel_id)),
            r'\(\);$': '',
            """CAS.*return "' \+ (\w+) \+ '";'\)\)""": r'return \1',
            r'this\.location\.href': 'thishref',
            r'new Image\(\);': ';',
        }

        for pattern, repl in replacements.items():
            src = re.sub(pattern, repl, src)

        eleven = execjs.compile(src)
        eleven_val = eleven.call('eleven')
        return eleven_val

    def __request_rooms(self, city_id, hotel_id, checkin, checkout, **kwargs):
        """ Request rooms info from ctrip.com.

        Args:
            city_id (int or str): ID of city.
            hotel_id (int or str): ID of hotel.
            checkin (str): check in date.
            checkout (str): check out date.
        """
        room_list_api = ('http://hotels.ctrip.com/Domestic/tool/'
                         'AjaxHote1RoomListForDetai1.aspx')

        callback = self.__gen_callback_t(16)
        timestamp = int(time.time() * 1000)
        content = self.__get_oceanball()
        eleven = self.__decrypt_oceanball(content, hotel_id)

        payload = {
            'EDM': 'F',
            'IncludeRoom': '',
            'IsDecoupleSpotHotelAndGroup': 'F',
            'IsFlash': 'F',
            'IsJustConfirm': '',
            'MasterHotelID': hotel_id,
            'RequestTravelMoney': 'F',
            '_': timestamp,
            'abForHuaZhu': '',
            'brand': 142,
            'callback': callback,
            'city': city_id,
            'contrast': 0,
            'contyped': 0,
            'couponList': '',
            'depDate': checkout,
            'eleven': eleven,
            'equip': '',
            'filter': '',
            'hotel': hotel_id,
            'hsids': '',
            'priceInfo': -1,
            'productcode': '',
            'psid': '',
            'roomId': '',
            'showspothotel': 'T',
            'startDate': checkin,
            'supplier': '',
        }

        for key, value in kwargs:
            if key in payload:
                payload[key] == value
            else:
                raise KeyError('Unrecongnized param {}'.format(key))

        response = requests.get(
            url=urljoin(self.base_url, room_list_api),
            params=payload,
            headers={
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Referer': 'http://hotels.ctrip.com/hotel/{}.html'
                       .format(hotel_id)})

        content = response.text
        content = json.loads(content)
        html = content['html']
        return html

    def __parse_rooms(self, html):
        """ Parse rooms info from html.

        Args:
            html (str): response after calling GET HotelRoomList

        Returns:
            Parsed rooms info.
        """
        html = etree.HTML(html)
        rooms = []
        for elem in html.iterfind('.//td[@data-baseroominfo]'):
            if elem.attrib['data-baseroominfo']:
                room = json.loads(elem.attrib['data-baseroominfo'])
                rooms.append(room)
        return rooms

    def __parse_quoted_prices(self, html):
        """ Parse quoted prices info from html.

        Args:
            html (str): response after calling GET HotelRoomList

        Returns:
            Parsed prices info.
        """
        html = etree.HTML(html)
        quoted_price = []
        for room_price in html.iterfind('.//a[@data-price]'):
            if room_price.attrib['tracevalue']:
                tracevalue = json.loads(room_price.attrib['tracevalue'])
                room_id = tracevalue['roomid']
                price = room_price.attrib['data-price']
                href = room_price.attrib['href']
                quoted_price.append({
                    'room_id': room_id,
                    'price': price,
                    'href': href})
        return quoted_price

    def __check_date_format(self, date):
        """ Check the date format.

        Args:
            date (str or datetime.date): input date.
        Returns:
            correct format date.
        Raises:
            Exception if input does not match the format.
        """
        if isinstance(date, datetime.date):
            return date.isoformat()
        if isinstance(date, str):
            if re.match(r'\d{4}-\d{2}-\d{2}', date):
                return date
        raise Exception("Input date {} doesn't follow correct "
                        "format 'yyyy-mm-dd'.".format(date))

    def get_rooms_and_prices(self, city_id, hotel_id, checkin='', checkout='',
                             **kwargs):
        """ Get all rooms info of specific hotel.

        Args:
            city_id (int): ID of city.
            hotel_id (int or str): ID of hotel.
            checkin (str or date): check in date.
            checkout (str or date): check out date.
        """
        if not checkin:
            checkin = datetime.date.today()
        if not checkout:
            checkout = checkin + datetime.timedelta(days=1)

        checkin = self.__check_date_format(checkin)
        checkout = self.__check_date_format(checkout)

        response = self.__request_rooms(city_id, hotel_id, checkin, checkout,
                                        **kwargs)
        rooms = self.__parse_rooms(response)
        quoted_prices = self.__parse_quoted_prices(response)
        return (rooms, quoted_prices)
