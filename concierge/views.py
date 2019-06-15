from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse

import random
import os
from django.utils import timezone
# Create your views here.
from .models import Location, Genre, Shop
from .modules import choice_shop

HOME_URL = 'https://tabelog.com/'


def index(request):
    locations = Location.objects.all()
    loc_top_00 = Location.objects.get(name='渋谷')
    loc_top_01 = Location.objects.get(name='新宿')
    # loc_tokyo = Location.objects.get(name='東京')
    loc_top_list = [loc_top_00, loc_top_01]
    return render(
        request,
        'concierge/index.html',
        {
            'loc_top_list': loc_top_list,
            'user': request.user})


def swipe(
        request, prefecture=None, region=None, district=None, station=None):
    area_str_list = ['prefecture', 'region', 'district', 'station']
    area_list = [prefecture, region, district, station]
    area_dict = dict(zip(area_str_list, area_list))
    location = get_object_or_404(Location, **area_dict)
    # ジャンルのリストを抽出。DBにないならスクレイピング。
    # genreの情報が古くなったら更新する機能をつけたい
    genre_list = Genre.objects.filter(location_name=location.name)
    if len(genre_list) == 0:
        # url_list = []
        # for area_url in area_list:
        #     if area_url is not None:
        #         url_list.append(area_url)
        # location.url = os.path.join(HOME_URL, *url_list) + '/'
        genre_dict = choice_shop.get_genre_dict(
            os.path.join(HOME_URL, location.url))
        for genre_url, genre_name in genre_dict.items():
            genre, created = Genre.objects.get_or_create(
                location_name=location.name,
                name=genre_name,
                url=genre_url,
                saved_date=timezone.now(),
            )
        genre_list = Genre.objects.filter(location_name=location.name)
    genre = random.choice(genre_list)
    shop_list = Shop.objects.filter(
        location_name=location.name, genre_name=genre.name)
    if len(shop_list) == 0:
        shop_dcit = choice_shop.get_shops_dict(genre.url)
        for shop_url, shop_elem_dict in shop_dcit.items():
            shop, created = Shop.objects.get_or_create(
                location_name=location.name,
                genre_name=genre.name,
                name=shop_elem_dict['nm'],
                url=shop_url,
                img_url=shop_elem_dict['img_url'],
                rank=shop_elem_dict['rank'],
                rate=shop_elem_dict['rate'],
                is_day=True,
                saved_date=timezone.now(),
            )
        shop_list = Shop.objects.filter(
            location_name=location.name, genre_name=genre.name)
    shop = random.choice(shop_list)
    return render(
        request, 'concierge/swipe.html', {
            'location': location,
            'genre': genre,
            'shop': shop, })


def choice_location(
        request, prefecture=None, region=None, district=None, station=None):
    """
    parent_locationをクリックしたらswipeの画面に移動
    child_locationをクリックしたらより詳細な地域を選択する画面に移動
    ただし、child_locationが一つもなかった場合はswipe画面に移動
    """
    area_str_list = ['prefecture', 'region', 'district', 'station']

    parent_area_list = [prefecture, region, district, station]
    parent_area_dict = dict(zip(area_str_list, parent_area_list))
    parent_location = get_object_or_404(Location, **parent_area_dict)
    # parent_url_list = []
    # for area in area_str_list:
    #     if parent_area_dict[area] is not None:
    #         parent_url_list.append(
    #             getattr(parent_location, area))
    # parent_location.url = os.path.join(*parent_url_list)

    child_area_dict = {}
    for key, value in parent_area_dict.items():
        if value is not None:
            child_area_dict[key] = value
    # これ以上child_locationがない場合はparent_locationのswipe画面に移動
    if len(child_area_dict) >= len(area_str_list):
        return redirect(
            os.path.join('/concierge/swipe/', parent_location.url))

    child_area_dict['level'] = area_str_list[len(child_area_dict)]
    child_locations = list(Location.objects.filter(**child_area_dict))
    print(child_locations, type(child_locations))

    # child_locationが一つもなかった場合はparent_locationのswipe画面に移動
    if len(child_locations) == 0:
        return redirect(
            os.path.join('/concierge/swipe/', parent_location.url))
    # 詳細な地域選択画面に移動
    for child_location in child_locations:
        url_ = []
        for i in range(len(child_area_dict)):
            url_.append(getattr(child_location, area_str_list[i]))
        child_location.url = os.path.join(*url_)
    return render(
        request, 'concierge/choice_location.html',
        {
            'user': request.user,
            'parent_location': parent_location,
            'child_locations': child_locations,
        }
    )