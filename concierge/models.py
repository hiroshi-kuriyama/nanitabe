from django.db import models
# Create your models here.


class Location(models.Model):
    # 場所の名前（日本語）
    name = models.CharField(max_length=128)
    # 地域のURL
    prefecture = models.CharField(max_length=64, blank=True, null=True)
    region = models.CharField(max_length=64, blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    station = models.CharField(max_length=64, blank=True, null=True)
    # 地域の階層（県、地区、駅など）
    level = models.CharField(max_length=64, blank=True, null=True)
    # urlを連結した文字列
    url = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    location_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    saved_date = models.DateTimeField()

    def __str__(self):
        return self.location_name + ' ' + self.name


class Shop(models.Model):
    location_name = models.CharField(max_length=128)
    genre_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    img_url = models.CharField(max_length=256)
    rank = models.IntegerField()
    rate = models.FloatField()
    is_day = models.BooleanField()
    saved_date = models.DateTimeField()

    def __str__(self):
        return self.location_name + ' ' + self.genre_name + ' ' + self.name