from django import template
from ..models import City

register = template.Library()

@register.simple_tag
def delete_city(city_now, city):
    print(city_now, city)
    City.objects.filter(city=city).delete()
    return 0