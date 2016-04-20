from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default = timezone.now
    )
    published_date = models.DateTimeField(
            blank = True, null = True
    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Laser(models.Model):
    dia = models.DecimalField(max_digits=8, decimal_places=5)
    power = models.DecimalField(max_digits=8, decimal_places=5)
    lam = models.DecimalField(max_digits=8, decimal_places=5)

    def get_dia(self):
        return self.dia

    def get_power(self):
        return self.power

    def get_lam(self):
        return self.lam
