import os
from time import sleep
import requests
from bs4 import BeautifulSoup

from ..models import Location

HOME_URL = 'https://tabelog.com/'


def get_region_dict(url_prefecture):
    region_dict = {}
    resp = requests.get(os.path.join(HOME_URL, url_prefecture))
    soup = BeautifulSoup(resp.text, 'html.parser')
    # 地域の要素を取得
    elems = soup.find_all('ul', class_="list-balloon__list-col")

    for i in range(4):
        e = elems[i]
        region_elems = e.find_all('a')
        for r_e in region_elems:
            url_region = r_e.get('href').split('/')[-2]
            region = r_e.find('span').getText()
            region_dict[region] = url_region
    return region_dict


def get_district_dict(url_prefecture, url_region):
    district_dict = {}
    resp = requests.get(os.path.join(HOME_URL, url_prefecture, url_region))
    soup = BeautifulSoup(resp.text, 'html.parser')
    # 地区の要素(li)を取得
    elems = soup.find_all('li', class_="list-balloon__list-item")

    for e in elems:
        url_district = e.find('a').get('href').split('/')[-2]
        district = e.find('a').find('span').getText()
        district_dict[district] = url_district
    return district_dict


def get_station_dict(url_prefecture, url_region, url_district):
    station_dict = {}
    resp = requests.get(os.path.join(
        HOME_URL, url_prefecture, url_region, url_district))
    soup = BeautifulSoup(resp.text, 'html.parser')
    # 駅の要素(li)を取得
    elems = soup.find_all('li', class_="list-balloon__list-item")

    for e in elems:
        url_station = e.find('a').get('href').split('/')[-3]
        station = e.find('a').find('span').getText()
        station_dict[station] = url_station
    return station_dict


def get_location_dict(url_prefecture):
    location_dict = {}
    location_dict['東京'] = {
        'prefecture': url_prefecture,
        'region': None,
        'district': None,
        'station': None,
        'level': 'prefecture'
    }
    region_dict = get_region_dict(url_prefecture)
    for region, url_region in region_dict.items():
        location_dict[region] = {
            'prefecture': url_prefecture,
            'region': url_region,
            'district': None,
            'station': None,
            'level': 'region'
        }
        district_dict = get_district_dict(url_prefecture, url_region)
        for district, url_district in district_dict.items():
            res = requests.get(os.path.join(
                HOME_URL, url_prefecture, url_region, url_district))
            if res.status_code == 404:
                continue
            location_dict[district] = {
                'prefecture': url_prefecture,
                'region': url_region,
                'district': url_district,
                'station': None,
                'level': 'district'
            }
            station_dict = get_station_dict(url_prefecture, url_region, url_district)
            for station, url_station in station_dict.items():
                res = requests.get(os.path.join(
                    HOME_URL, url_prefecture, url_region, url_district, url_station) + '/')
                if res.status_code == 404:
                    continue
                location_dict[station] = {
                    'prefecture': url_prefecture,
                    'region': url_region,
                    'district': url_district,
                    'station': url_station,
                    'level': 'station'
                }
            sleep(1)
    for location_name, _ in location_dict.items(): 
        location = location_dict[location_name]
        area_str_list = ['prefecture', 'region', 'district', 'station']
        part_urls = [location[i] for i in area_str_list if location[i] is not None]
        location['url'] = os.path.join(*part_urls) + '/'
    return location_dict


def save_locations(location_dict):
    for name, url_dict in location_dict.items():
        location, created = Location.objects.get_or_create(name=name)
        location.name = name
        location.prefecture = url_dict['prefecture']
        location.region = url_dict['region']
        location.district = url_dict['district']
        location.station = url_dict['station']
        location.level = url_dict['level']
        location.url = url_dict['url']
        location.save()


def test():
    location_dict_test = {
        '銀座・新橋・有楽町': {
            'prefecture': 'tokyo',
            'region': 'A1301',
            'district': None,
            'station': None,
            'level': 'region',},
        '銀座': {
            'prefecture': 'tokyo',
            'region': 'A1301',
            'district': 'A130101',
            'station': None,
            'level': 'district'},
        '銀座駅': {
            'prefecture': 'tokyo',
            'region': 'A1301',
            'district': 'A130101',
            'station': 'R3368',
            'level': 'station'}}
    save_locations(location_dict_test)
    print(Location.objects.all())


def run():
    location_dict = get_location_dict(url_prefecture='tokyo')
    save_locations(location_dict)