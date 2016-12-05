import requests
import json
import time

class Ctrip(object):

    def get_hotel_list(self, cityId='', star=0, counts=0):
        response = self._request_hotels_list(cityId=cityId, star=star)
        total_amount = response['hotelAmount']
        if counts >= total_amount:
            print('Only {} hotels match all conditions, input {} exceeds.'
                  .format(total_amount, counts))
            counts = total_amount
        elif counts == 0:
            counts = total_amount

        hotels_name = []
        for page in range(1, (counts-1)//25+2):
            time.sleep(3)
            print('Downloading Page {}....'.format(page))
            response = self._request_hotels_list(cityId=cityId, star=star, page=page)
            if len(response['hotelPositionJSON']) == 0:
                break
            for hotel_detail in response['hotelPositionJSON']:
                hotels_name.append(hotel_detail['name'])
        return hotels_name

    def _request_hotels_list(self, cityId='', page=1, star=0):

        response = requests.post(
            url='http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
            'star': star,
            'cityId': cityId,
            'page': page,#page, # 25 items per page
            }
        )

        response = json.loads(response.text)
        return response

if __name__ == '__main__':

    hotels = Ctrip().get_hotel_list(cityId=2, star=5, counts=10)
    for hotel in hotels:
        print(hotel)

