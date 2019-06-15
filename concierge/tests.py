from django.test import TestCase

# Create your tests here.
if False:
    from concierge.models import Location
    location_dict = {
        'nishi-shinjuku': 'https://tabelog.com/tokyo/A1304/A130401/R7443/rstLst/',
        'ヒカリエ': 'https://tabelog.com/tokyo/A1303/A130301/R4698/rstLst/',
        }
    for location_name, location_url in location_dict.items():
        Location.objects.create(location_name=location_name, location_url=location_url)