from django.contrib import admin
from .models import Station


class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ('username', 'position', 'position_map',)

    def position_map(self, instance):
        if instance.position is not None:
            return '<img src="http://maps.googleapis.com/maps/api/staticmap?center=%(latlong)s&zoom=%(zoom)s&size=%(width)sx%(hei)s&maptype=roadmap&markers=%(latlong)s&sensor=false&visual_refresh=true&scale=%(scale)s" width="%(width)s" height="%(height)s">' % {
                'latlong': instance.position,
                'zoom': 15,
                'width': 100,
                'height': 100,
                'scale': 2
            }
    position_map.allow_tags = True


admin.site.register(Station, PointOfInterestAdmin)
