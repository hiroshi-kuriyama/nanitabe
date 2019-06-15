import json
import random
import requests
from bs4 import BeautifulSoup


def get_genre_dict(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # ジャンルの要素(li)を取得
    elems = soup.find_all('li', class_="list-balloon__btn-item")
    # 各ジャンルのURLとジャンル名を辞書に保存
    genres = []
    urls = []
    for e in elems:
        if e.find('a') is not None:
            genres.append(e.getText()[24:-22])
            urls.append(e.find('a').get('href'))
    genre_dict = dict(zip(urls, genres))
    return genre_dict


def get_shops_dict(genre_url):
    # ジャンルのURLをランチ2000円以内ランキングのURLに修正
    genre_rank_url = genre_url + \
        "?SrtT=rt&LstCosT=2&RdoCosTp=1&Srt=D&sort_mode=1"
    resp = requests.get(genre_rank_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # 店舗ごとに分割
    elems = soup.find_all(
        'li',
        class_="list-rst js-bookmark js-rst-cassette-wrap list-rst--ranking")
    # 各店舗のURLに店舗情報の辞書を作成し紐付ける
    # 店舗情報は店名、ランキング、画像、星の数
    shops_dict = {}
    for e in elems:
        e_sum = e.find(
            'a',
            class_='list-rst__rst-name-target cpy-rst-name js-ranking-num')
        e_img = e.find(
            'img',
            class_="js-cassette-img cpy-main-image")
        e_rate = e.find(
            'span',
            class_="c-rating__val c-rating__val--strong list-rst__rating-val")
        shop_elem_dict = {
            'nm': e_sum.getText(),
            'rank': int(e_sum.get('data-ranking')),
            'img_url': e_img.get('data-original'),
            'rate': float(e_rate.getText())
        }
        shops_dict[e_sum.get('href')] = shop_elem_dict
    return shops_dict