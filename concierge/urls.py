from django.urls import path

from . import views

app_name = 'concierge'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:location_name>/', views.swipe, name='swipe'),
    path(
        'choice_location/<str:prefecture>/',
        views.choice_location, name='choice_location'),
    path(
        'choice_location/<str:prefecture>/<str:region>/',
        views.choice_location, name='choice_location'),
    path(
        'choice_location/<str:prefecture>/<str:region>/<str:district>/',
        views.choice_location, name='choice_location'),
    path(
        'choice_location/<str:prefecture>/<str:region>/<str:district>/<str:station>/',
        views.choice_location, name='choice_location'),
    path(
        'swipe/<str:prefecture>/',
        views.swipe, name='swipe'),
    path(
        'swipe/<str:prefecture>/<str:region>/',
        views.swipe, name='swipe'),
    path(
        'swipe/<str:prefecture>/<str:region>/<str:district>/',
        views.swipe, name='swipe'),
    path(
        'swipe/<str:prefecture>/<str:region>/<str:district>/<str:station>/',
        views.swipe, name='swipe'),
]