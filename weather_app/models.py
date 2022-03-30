from django.db import models


class City(models.Model):

    city = models.SlugField(max_length=50)

    def __str__(self):
        return self.city
