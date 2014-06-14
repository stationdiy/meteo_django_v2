from django.db import models
from django_google_maps import fields as map_fields
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User
from django.db import models

class Usuario(User):
    name = models.CharField(max_length=30)
    telefono = models.PositiveIntegerField(null=True, blank=True)
    amigos = models.ManyToManyField('self', symmetrical=True,  blank=True)
    USERNAME_FIELD = 'email'
class Station(models.Model):

    username = models.ForeignKey(User)
    MAC = models.CharField(unique=True, max_length=30)
    address = models.CharField(null=True,max_length=200)
    country = models.CharField(null=True,max_length=20)
    city=models.CharField(null=True,max_length=20)
    position = GeopositionField(null=True)
    temperatura=models.FloatField(null=True)
    humedad=models.FloatField(null=True)
    actioner1=models.BooleanField()
    actioner2=models.BooleanField()
    actioner3=models.BooleanField()
    def __unicode__(self):
    	return u'%s %s' % (self.MAC,self.city)
    class Meta:
        verbose_name_plural = 'points of interest'
    	

